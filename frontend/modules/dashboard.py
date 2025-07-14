from plotly.subplots import make_subplots

import plotly.graph_objs as go

class Dashboard:
  def __init__(self, scenario, solution):
    self.scenario = scenario
    self.solution = solution

  def plot_route_distribution(self):
    # Exemplo: Distribuição de passageiros por rota
    routes = [route.name for route in self.scenario.routes]
    passengers = [self.solution.route_passengers[route.name] for route in self.scenario.routes]

    fig = go.Figure([go.Bar(x=routes, y=passengers)])
    fig.update_layout(title="Passageiros por Rota", xaxis_title="Rota", yaxis_title="Passageiros")
    return fig

  def plot_vehicle_utilization(self):
    # Exemplo: Utilização dos veículos
    vehicles = [v.id for v in self.scenario.vehicles]
    utilization = [self.solution.vehicle_utilization[v.id] for v in self.scenario.vehicles]

    fig = go.Figure([go.Bar(x=vehicles, y=utilization)])
    fig.update_layout(title="Utilização dos Veículos", xaxis_title="Veículo", yaxis_title="Utilização (%)")
    return fig

  def plot_summary(self):
    # Exemplo: Resumo em subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Passageiros por Rota", "Utilização dos Veículos"))

    # Passageiros por rota
    routes = [route.name for route in self.scenario.routes]
    passengers = [self.solution.route_passengers[route.name] for route in self.scenario.routes]
    fig.add_trace(go.Bar(x=routes, y=passengers), row=1, col=1)

    # Utilização dos veículos
    vehicles = [v.id for v in self.scenario.vehicles]
    utilization = [self.solution.vehicle_utilization[v.id] for v in self.scenario.vehicles]
    fig.add_trace(go.Bar(x=vehicles, y=utilization), row=1, col=2)

    fig.update_layout(title_text="Resumo do Cenário e Solução")
    return fig