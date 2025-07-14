from flask import Blueprint, jsonify, request
from app.services.solver_service import SolverService

bp = Blueprint("solver", __name__, url_prefix="/api/solver")
solver_service = SolverService()

@bp.route("/run-static-model", methods=["POST"])
def run_static_model():
    data = request.json
    user_id = data.get( "user_id" )
    scenario_id = data.get( "scenario_id" )
    M = data.get("M")

    try:
        result = solver_service.run_model_linearized_static(user_id, scenario_id, M)
        return jsonify({"success": True, "result": result}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500
