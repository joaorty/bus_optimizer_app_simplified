from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.route_repository import RouteRepository
from app.repositories.solution_repository import SolutionRepository
from app.repositories.bus_type_repository import BusTypeRepository
from app.repositories.parameters_repository import ParametersRepository

class RepositoryManager:
    """
    Singleton para controlar todos os repositórios do sistema de transporte.

    Benefícios:
    - Evita múltiplas instâncias de cada repositório;
    - Centraliza os acessos aos dados;
    - Facilita os imports e promove desacoplamento.
    """

    _scenario_repository: ScenarioRepository = None
    _route_repository: RouteRepository = None
    _solution_repository: SolutionRepository = None
    _bus_type_repository: BusTypeRepository = None
    _parameters_repository: ParametersRepository = None

    _repositories = {}

    @staticmethod
    def get_scenario_repository() -> ScenarioRepository:
        if RepositoryManager._scenario_repository is None:
            RepositoryManager._scenario_repository = ScenarioRepository()
            RepositoryManager._repositories["ScenarioRepository"] = RepositoryManager._scenario_repository
        return RepositoryManager._scenario_repository

    @staticmethod
    def get_route_repository() -> RouteRepository:
        if RepositoryManager._route_repository is None:
            RepositoryManager._route_repository = RouteRepository()
            RepositoryManager._repositories["RouteRepository"] = RepositoryManager._route_repository
        return RepositoryManager._route_repository

    @staticmethod
    def get_solution_repository() -> SolutionRepository:
        if RepositoryManager._solution_repository is None:
            RepositoryManager._solution_repository = SolutionRepository()
            RepositoryManager._repositories["SolutionRepository"] = RepositoryManager._solution_repository
        return RepositoryManager._solution_repository

    @staticmethod
    def get_bus_type_repository() -> BusTypeRepository:
        if RepositoryManager._bus_type_repository is None:
            RepositoryManager._bus_type_repository = BusTypeRepository()
            RepositoryManager._repositories["BusTypeRepository"] = RepositoryManager._bus_type_repository
        return RepositoryManager._bus_type_repository

    @staticmethod
    def get_parameters_repository() -> ParametersRepository:
        if RepositoryManager._parameters_repository is None:
            RepositoryManager._parameters_repository = ParametersRepository()
            RepositoryManager._repositories["ParametersRepository"] = RepositoryManager._parameters_repository
        return RepositoryManager._parameters_repository

    @staticmethod
    def get_repository_by_name(name: str):
        """
        Retorna um repositório pelo nome da classe.
        """
        if name not in RepositoryManager._repositories:
            RepositoryManager._repositories[name] = globals()[name]()
        return RepositoryManager._repositories[name]
