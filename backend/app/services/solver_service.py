import pulp
from math import ceil, floor

from app.models import Solution
from app.models.solution_model import SolutionStatus
from app.repositories import RepositoryManager

class SolverService:
    def __init__(self):
        self.parameters_repo = RepositoryManager.get_parameters_repository()
        self.route_repo = RepositoryManager.get_route_repository()
        self.bus_type_repo = RepositoryManager.get_bus_type_repository()
        self.solution_repo = RepositoryManager.get_solution_repository()
        self.scenario_repo = RepositoryManager.get_scenario_repository()

    def extract_scenario_data(self, scenario_id):
        """Extrai dados do cenário usando repositórios"""
        params = self.parameters_repo.find_first_by( scenario_id=scenario_id )
        if not params:
            raise ValueError("Parameters not found for scenario")

        routes = self.route_repo.find_all_by( scenario_id=scenario_id )
        if not routes:
            raise ValueError("Routes not found for scenario")

        bus_types = self.bus_type_repo.find_all_by( scenario_id=scenario_id )
        if not bus_types:
            raise ValueError("Bus types not found for scenario")

        P = int( params.units_time )
        W = float( params.wait_cost )
        Ctran = int( params.acceptable_time_transfer )
        Caglo = int( params.agglomeration_cost )

        R = [route.id for route in routes]
        B = [bus.id for bus in bus_types]

        CC = {route.id: int( route.length_km ) for route in routes}
        TC = {route.id: int( route.time_minutes ) for route in routes}
        Qmax = {route.id: int( route.passengers ) for route in routes}

        CAP = {bus.id: int( bus.seat_capacity ) for bus in bus_types}
        Cope = {bus.id: float( bus.operational_cost_km ) for bus in bus_types}
        FCmax = {bus.id: float( bus.load_factor ) for bus in bus_types}
        FT = {bus.id: int( bus.available_units ) for bus in bus_types}

        Cesp = 1.0

        return P, W, R, B, CC, TC, Qmax, CAP, Cope, FCmax, Cesp, Caglo, Ctran, FT

    def common_variables_static(self, B, R):
        """Cria variáveis comuns do modelo estático"""
        v = pulp.LpVariable.dicts("v", [(b, r) for b in B for r in R], lowBound=0, cat='Integer')
        f = pulp.LpVariable.dicts("f", [(b, r) for b in B for r in R], lowBound=0, cat='Continuous')
        q = pulp.LpVariable.dicts("q", [(b, r) for b in B for r in R], lowBound=0, cat='Continuous')
        y = pulp.LpVariable.dicts("y", R, cat='Binary')
        u = pulp.LpVariable.dicts("u", B, lowBound=0, cat='Integer')
        e = pulp.LpVariable.dicts("e", [(b, r) for b in B for r in R], lowBound=0, cat='Continuous')
        w = pulp.LpVariable.dicts("w", R, lowBound=0, cat='Continuous')
        z = pulp.LpVariable.dicts("z", R, lowBound=0, cat='Continuous')
        H = pulp.LpVariable.dicts("H", R, lowBound=0, cat='Continuous')
        return v, f, q, y, u, e, w, z, H

    def run_model_linearized_static(self, user_id: int, scenario_id: int, M=1e4):
        """Executa o modelo linearizado estático"""

        # Verificações de parâmetros obrigatórios
        if user_id is None or not isinstance(user_id, int):
            raise ValueError("user_id must be provided and must be an integer.")
        if scenario_id is None or not isinstance(scenario_id, int):
            raise ValueError("scenario_id must be provided and must be an integer.")
        if M is None or not isinstance(M, (int, float)) or M <= 0:
            raise ValueError("M must be a positive number.")

        # Verifica se o cenário pertence ao usuário
        scenario = self.scenario_repo.get_by_id(scenario_id)
        if not scenario or scenario.user_id != user_id:
            raise ValueError("Scenario not found or access denied.")
        
        P, W, R, B, CC, TC, Qmax, CAP, Cope, FCmax, Cesp, Caglo, Ctran, FT = self.extract_scenario_data(scenario_id)

        model = pulp.LpProblem("Static_Bus_Allocation", pulp.LpMinimize)
        v, f, q, y, u, e, w, z, H = self.common_variables_static(B, R)

        alpha = 5
        effective_capacity = [round(FCmax[b] * CAP[b]) for b in B]
        min_effective_capacity = min(effective_capacity)
        total_fleet = int(sum(FT[b] for b in B))

        k_max = {}
        for r in R:
            if P < TC[r]:
                k_max[r] = min(ceil(Qmax[r] / min_effective_capacity) * alpha, total_fleet)
            else:
                k_max[r] = min(
                    ceil(Qmax[r] / min_effective_capacity) * alpha,
                    total_fleet,
                    floor(P / TC[r]) * total_fleet
                )

        K_total = {r: list(range(1, k_max[r] + 1)) for r in R}
        delta_tot = pulp.LpVariable.dicts("delta_tot", [(k, r) for r in R for k in K_total[r]], cat='Binary')

        # Objetivo
        objective = 0
        for b in B:
            for r in R:
                objective += Cope[b] * CC[r] * f[(b, r)]

        for r in R:
            objective += (H[r] / 2) * Cesp

        for b in B:
            for r in R:
                objective += e[(b, r)] * Caglo

        for r in R:
            objective += Ctran * w[r] + M * z[r]

        model += objective

        # Restrições
        for r in R:
            model += pulp.lpSum(f[(b, r)] for b in B) == pulp.lpSum(k * delta_tot[(k, r)] for k in K_total[r])
            model += pulp.lpSum((P / k) * delta_tot[(k, r)] for k in K_total[r]) == H[r]
            model += (H[r] / 2 <= W + (P - W) * y[r])
            model += pulp.lpSum(delta_tot[(k, r)] for k in K_total[r]) == 1
            model += w[r] <= pulp.lpSum(q[(b, r)] for b in B)
            model += w[r] <= Qmax[r] * y[r]
            model += w[r] >= pulp.lpSum(q[(b, r)] for b in B) - Qmax[r] * (1 - y[r])
            model += z[r] == Qmax[r] - pulp.lpSum(q[(b, r)] for b in B)

        for b in B:
            for r in R:
                model += q[(b, r)] <= FCmax[b] * CAP[b] * f[(b, r)]
                model += e[(b, r)] >= q[(b, r)] - CAP[b] * f[(b, r)]
                model += e[(b, r)] >= 0
                model += v[(b, r)] == f[(b, r)] if TC[r] > P else v[(b, r)] == floor(P / TC[r]) * f[(b, r)]

        for r in R:
            model += pulp.lpSum(q[(b, r)] for b in B) <= Qmax[r]

        for b in B:
            model += pulp.lpSum(v[(b, r)] for r in R) <= FT[b]
            model += u[b] == pulp.lpSum(v[(b, r)] for r in R)
            model += u[b] <= FT[b]

        # Resolver modelo
        model.solve()

        if model.status != pulp.LpStatusOptimal:
            raise RuntimeError(f"Optimization failed with status: {pulp.LpStatus[model.status]}")

        # Extrair dados da solução
        solution_data = {
            "variables": {
                "v": {f"{b}_{r}": pulp.value(v[(b, r)]) for b in B for r in R},
                "f": {f"{b}_{r}": pulp.value(f[(b, r)]) for b in B for r in R},
                "q": {f"{b}_{r}": pulp.value(q[(b, r)]) for b in B for r in R},
                "y": {str(r): pulp.value(y[r]) for r in R},
                "u": {str(b): pulp.value(u[b]) for b in B},
                "w": {str(r): pulp.value(w[r]) for r in R},
                "z": {str(r): pulp.value(z[r]) for r in R},
                "H": {str(r): pulp.value(H[r]) for r in R}
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

        # Criar e salvar a solução
        solution = Solution(
            scenario_id=scenario_id,
            status=SolutionStatus.completed,
            objective_value=pulp.value(model.objective),
            solution_data=solution_data,
            parameters_solution=parameters_solution
        )

        self.solution_repo.save( solution )

        # Resultados
        return {
            "status": "Completed",
            "objective_value": pulp.value(model.objective),
            "solution_data": solution_data,
            "parameters_solution": parameters_solution
        }
