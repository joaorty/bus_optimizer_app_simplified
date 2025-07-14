from flask import Flask

from app.controllers.solver_controller import bp as solver_bp
from app.controllers.scenario_controller import bp as scenario_bp
from app.controllers.auth_controller import bp as auth_bp
from app.controllers.user_controller import bp as user_bp

def register_routes( app : Flask ):
    app.register_blueprint( solver_bp )
    app.register_blueprint( scenario_bp )
    app.register_blueprint( auth_bp )
    app.register_blueprint( user_bp )