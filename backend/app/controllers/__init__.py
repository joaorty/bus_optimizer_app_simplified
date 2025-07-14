from flask import Flask

from app.controllers.solver_controller import bp as solver_bp

def register_routes( app : Flask ):
    app.register_blueprint( solver_bp )