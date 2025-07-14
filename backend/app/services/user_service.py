from app.models import SolverUser
from app.repositories import RepositoryManager
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def __init__(self):
        self.user_repository = RepositoryManager.get_user_repository()
        self.scenario_repository = RepositoryManager.get_scenario_repository()

    # === CRUD ===
    def create_user(self, name: str, username: str, password: str):
        if not username:
            raise ValueError("The username must be passed!")
        if not password:
            raise ValueError("A password must be passed!")

        if self.verify_user(username):
            raise ValueError(f"SolverUser '{username}' already exists.")

        hashed_password = generate_password_hash(password)
        new_user = SolverUser(name=name, username=username, password=hashed_password)
        self.user_repository.save(new_user)

        return self._clean_user_dict(new_user)

    def delete_user_by_id(self, user_id: int):
        if not self.verify_id(user_id):
            raise ValueError(f"SolverUser '{user_id}' does not exist.")

        user = self.user_repository.get_by_id(user_id)
        self.user_repository.delete(user)
        return self._clean_user_dict(user)

    def delete_user_by_username(self, username: str):
        if not self.verify_user(username):
            raise ValueError(f"SolverUser '{username}' does not exist.")

        user = self.user_repository.find_by_username(username)
        self.user_repository.delete(user)
        return self._clean_user_dict(user)

    def update_user_by_id(self, user_id: int, new_username: str, new_password: str):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"SolverUser '{user_id}' does not exist.")

        if new_username != user.username and self.verify_user(new_username):
            raise ValueError(f"SolverUser '{new_username}' already exists.")

        user.username = new_username
        user.password = generate_password_hash(new_password)
        updated_user = self.user_repository.update(user)
        return self._clean_user_dict(updated_user)

    def update_user_by_username(self, old_username: str, new_username: str, new_password: str):
        if not self.verify_user(old_username):
            raise ValueError(f"SolverUser '{old_username}' does not exist.")
        if self.verify_user(new_username):
            raise ValueError(f"SolverUser '{new_username}' already exists.")

        user = self.user_repository.find_by_username(old_username)
        user.username = new_username
        user.password = generate_password_hash(new_password)
        updated_user = self.user_repository.update(user)
        return self._clean_user_dict(updated_user)

    # === Acesso ===
    def login(self, username: str, password: str):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Invalid username. It must be a non-empty string.")
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Invalid password. It must be a non-empty string.")

        user = self.user_repository.find_by_username(username)
        if user and check_password_hash(user.password, password):
            return self._clean_user_dict(user)

        raise ValueError("Invalid username or password.")

    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("SolverUser not found.")
        return self._clean_user_dict(user)

    def get_user_by_username(self, username: str):
        user = self.user_repository.find_by_username(username)
        if not user:
            raise ValueError("SolverUser not found.")
        return self._clean_user_dict(user)

    def get_all_users(self):
        users = self.user_repository.get_all()
        return [self._clean_user_dict(user) for user in users]

    # === Recursos Relacionados ===
    def get_user_scenarios(self, user_id: int):
        if not self.verify_id(user_id):
            raise ValueError("SolverUser not found.")

        scenarios = self.scenario_repository.find_by(user_id=user_id)
        if not scenarios:
            raise ValueError("No scenarios found for the given user.")

        return [sim.to_dict() for sim in scenarios]

    def get_user_parameters(self, user_id: int):
        if not self.verify_id(user_id):
            raise ValueError("")
