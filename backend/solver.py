import pulp
from math import ceil, floor
from sqlalchemy.orm import sessionmaker, Session


# Função para extrair dados do cenário
def extract_scenario_data(scenario_id: int, db: Session):
    """Extrai dados do cenário do banco de dados"""
    
    # Buscar parâmetros
    params = db.query(ParametersModel).filter(ParametersModel.scenario_id == scenario_id).first()
    if not params:
        raise HTTPException(status_code=404, detail="Parameters not found for scenario")
    
    # Buscar rotas
    routes = db.query(RouteModel).filter(RouteModel.scenario_id == scenario_id).all()
    if not routes:
        raise HTTPException(status_code=404, detail="Routes not found for scenario")
    
    # Buscar tipos de ônibus
    bus_types = db.query(BusTypeModel).filter(BusTypeModel.scenario_id == scenario_id).all()
    if not bus_types:
        raise HTTPException(status_code=404, detail="Bus types not found for scenario")
    
    # Converter para formato esperado pelo modelo
    P = params.units_time  # Período de tempo
    W = params.wait_cost  # Custo de espera
    Ctran = params.acceptable_time_transfer  # Tempo aceitável de transferência
    Caglo = params.agglomeration_cost  # Custo de aglomeração
    
    # Criar conjuntos de índices
    R = [route.id for route in routes]  # Conjunto de rotas
    B = [bus.id for bus in bus_types]  # Conjunto de tipos de ônibus
    
    # Criar dicionários de dados
    CC = {route.id: route.length_km for route in routes}  # Comprimento das rotas
    TC = {route.id: route.time_minutes for route in routes}  # Tempo de ciclo
    Qmax = {route.id: route.passengers for route in routes}  # Demanda máxima
    
    CAP = {bus.id: bus.seat_capacity for bus in bus_types}  # Capacidade dos ônibus
    Cope = {bus.id: bus.operational_cost_km for bus in bus_types}  # Custo operacional
    FCmax = {bus.id: bus.load_factor for bus in bus_types}  # Fator de carga
    FT = {bus.id: bus.available_units for bus in bus_types}  # Frota disponível
    
    # Valores padrão (ajuste conforme necessário)
    Cesp = 1.0  # Custo de espera
    
    return P, W, R, B, CC, TC, Qmax, CAP, Cope, FCmax, Cesp, Caglo, Ctran, FT

# Função do modelo de otimização
def common_variables_static(B, R):
    """Cria variáveis comuns do modelo estático"""
    v = pulp.LpVariable.dicts("v", [(b, r) for b in B for r in R], 
                              lowBound=0, cat='Integer')
    f = pulp.LpVariable.dicts("f", [(b, r) for b in B for r in R], 
                              lowBound=0, cat='Continuous')
    q = pulp.LpVariable.dicts("q", [(b, r) for b in B for r in R], 
                              lowBound=0, cat='Continuous')
    y = pulp.LpVariable.dicts("y", R, cat='Binary')
    u = pulp.LpVariable.dicts("u", B, lowBound=0, cat='Integer')
    e = pulp.LpVariable.dicts("e", [(b, r) for b in B for r in R], 
                              lowBound=0, cat='Continuous')
    w = pulp.LpVariable.dicts("w", R, lowBound=0, cat='Continuous')
    z = pulp.LpVariable.dicts("z", R, lowBound=0, cat='Continuous')
    H = pulp.LpVariable.dicts("H", R, lowBound=0, cat='Continuous')
    return v, f, q, y, u, e, w, z, H

def run_model_linearized_static(scenario_id: int, db: Session, M: float = 1e4):
    """Executa o modelo linearizado estático usando PuLP"""
    
    try:
        # Extrair dados do cenário
        P, W, R, B, CC, TC, Qmax, CAP, Cope, FCmax, Cesp, Caglo, Ctran, FT = extract_scenario_data(scenario_id, db)
        
        # Criar modelo
        model = pulp.LpProblem("Static_Bus_Allocation", pulp.LpMinimize)
        
        # Variáveis principais
        v, f, q, y, u, e, w, z, H = common_variables_static(B, R)
        
        # Parâmetros
        alpha = 5
        effective_capacity = [round(FCmax[b] * CAP[b]) for b in B]
        min_effective_capacity = min(effective_capacity)
        total_fleet = int(sum(FT[b] for b in B))
        
        # Cálculo de k_max
        k_max = {}
        for r in R:
            if P < TC[r]:
                k_max[r] = min(
                    ceil(Qmax[r] / min_effective_capacity) * alpha,
                    total_fleet
                )
            else:
                k_max[r] = min(
                    ceil(Qmax[r] / min_effective_capacity) * alpha,
                    total_fleet,
                    floor(P / TC[r]) * total_fleet
                )
        
        K_total = {r: list(range(1, k_max[r] + 1)) for r in R}
        
        # Variáveis delta_tot
        delta_tot = pulp.LpVariable.dicts("delta_tot", 
                                         [(k, r) for r in R for k in K_total[r]], 
                                         cat='Binary')
        
        # Função objetivo
        objective = 0
        
        # Termos da função objetivo
        for b in B:
            for r in R:
                objective += Cope[b] * CC[r] * f[(b, r)]
        
        for r in R:
            objective += (H[r] / 2) * Cesp
        
        for b in B:
            for r in R:
                objective += e[(b, r)] * Caglo
        
        for r in R:
            objective += Ctran * w[r]
        
        for r in R:
            objective += M * z[r]
        
        model += objective
        
        # Restrições
        for r in R:
            model += (
                pulp.lpSum(f[(b, r)] for b in B) == 
                pulp.lpSum(k * delta_tot[(k, r)] for k in K_total[r])
            )
        
        for r in R:
            model += (
                pulp.lpSum((P / k) * delta_tot[(k, r)] for k in K_total[r]) == H[r]
            )
        
        for r in R:
            model += (H[r] / 2 <= W + (P - W) * y[r])
        
        for r in R:
            model += (pulp.lpSum(delta_tot[(k, r)] for k in K_total[r]) == 1)
        
        for r in R:
            model += w[r] <= pulp.lpSum(q[(b, r)] for b in B)
            model += w[r] <= Qmax[r] * y[r]
            model += w[r] >= pulp.lpSum(q[(b, r)] for b in B) - Qmax[r] * (1 - y[r])
        
        for r in R:
            model += z[r] == Qmax[r] - pulp.lpSum(q[(b, r)] for b in B)
        
        for b in B:
            for r in R:
                model += q[(b, r)] <= FCmax[b] * CAP[b] * f[(b, r)]
                
                if TC[r] > P:
                    model += v[(b, r)] == f[(b, r)]
                else:
                    model += v[(b, r)] == floor(P / TC[r]) * f[(b, r)]
                
                model += e[(b, r)] >= q[(b, r)] - CAP[b] * f[(b, r)]
                model += e[(b, r)] >= 0
        
        for r in R:
            model += pulp.lpSum(q[(b, r)] for b in B) <= Qmax[r]
        
        for b in B:
            model += pulp.lpSum(v[(b, r)] for r in R) <= FT[b]
            model += u[b] == pulp.lpSum(v[(b, r)] for r in R)
            model += u[b] <= FT[b]
        
        # Resolver modelo
        model.solve()
        
        # Processar resultados
        if model.status == pulp.LpStatusOptimal:
            # Extrair valores das variáveis
            solution_data = {
                "variables": {
                    "v": {f"{b}_{r}": pulp.value(v[(b, r)]) for b in B for r in R if pulp.value(v[(b, r)]) is not None},
                    "f": {f"{b}_{r}": pulp.value(f[(b, r)]) for b in B for r in R if pulp.value(f[(b, r)]) is not None},
                    "q": {f"{b}_{r}": pulp.value(q[(b, r)]) for b in B for r in R if pulp.value(q[(b, r)]) is not None},
                    "y": {str(r): pulp.value(y[r]) for r in R if pulp.value(y[r]) is not None},
                    "u": {str(b): pulp.value(u[b]) for b in B if pulp.value(u[b]) is not None},
                    "w": {str(r): pulp.value(w[r]) for r in R if pulp.value(w[r]) is not None},
                    "z": {str(r): pulp.value(z[r]) for r in R if pulp.value(z[r]) is not None},
                    "H": {str(r): pulp.value(H[r]) for r in R if pulp.value(H[r]) is not None}
                }
            }
            
            parameters_solution = {
                "P": P,
                "W": W,
                "alpha": alpha,
                "M": M,
                "total_fleet": total_fleet,
                "k_max": k_max
            }
            
            return {
                "status": "Completed",
                "objective_value": pulp.value(model.objective),
                "solution_data": solution_data,
                "parameters_solution": parameters_solution
            }
        else:
            return {
                "status": "Failed",
                "objective_value": None,
                "solution_data": {"error": f"Optimization failed with status: {pulp.LpStatus[model.status]}"},
                "parameters_solution": None
            }
    
    except Exception as e:
        return {
            "status": "Failed",
            "objective_value": None,
            "solution_data": {"error": str(e)},
            "parameters_solution": None
        }