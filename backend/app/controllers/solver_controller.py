from flask import Blueprint, jsonify, request
from app.services.solver_service import SolverService
from app.services.scenario_service import ScenarioService

bp = Blueprint("solver", __name__, url_prefix="/api/solver")
solver_service = SolverService()
scenario_service = ScenarioService()

@bp.route("/run-static-model", methods=["POST"])
def run_static_model():
    data = request.json
    user_id = data.get( "user_id" )
    
    scenario = scenario_service.create(
        user_id, data.get( "name_scenario" ), "Descrição genérica", 
        data.get( "routes" ), data.get( "bus_types" ), data.get( "parameters" )
    )

    try:
        result = solver_service.run_model_linearized_static(user_id, scenario.get( "id" ))
        return jsonify({"success": True, "result": result}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500
