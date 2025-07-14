from flask import Blueprint, jsonify, request
from app.services.solver_service import SolverService
from app import db  # sua instância do SQLAlchemy (flask_sqlalchemy)

bp = Blueprint("solver", __name__, url_prefix="/api/solver")
solver_service = SolverService()

@bp.route("/run-static-model", methods=["POST"])
def run_static_model():
    data = request.json
    scenario_id = data.get("scenario_id")

    if not isinstance(scenario_id, int):
        return jsonify({"error": "scenario_id must be an integer."}), 400

    try:
        result = solver_service.run_model_linearized_static(scenario_id, db.session)
        return jsonify({"success": True, "result": result}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500
