from flask import Blueprint, jsonify, request
from app.services.scenario_service import ScenarioService
from app import db  # instância do SQLAlchemy

bp = Blueprint("scenario", __name__, url_prefix="/api/scenarios")
scenario_service = ScenarioService()

@bp.route("/create", methods=["POST"])
def create_scenario():
    data = request.json
    name = data.get("name")
    description = data.get("description")

    if not name or not isinstance(name, str):
        return jsonify({"error": "Name is required and must be a string."}), 400

    try:
        scenario = scenario_service.create(db.session, name=name, description=description)
        return jsonify({"success": True, "scenario": scenario}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/get/<int:scenario_id>", methods=["GET"])
def get_scenario(scenario_id):
    try:
        scenario = scenario_service.get_by_id(db.session, scenario_id)
        return jsonify({"success": True, "scenario": scenario}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/get_all", methods=["GET"])
def get_all_scenarios():
    try:
        scenarios = scenario_service.get_all(db.session)
        return jsonify({"success": True, "scenarios": scenarios}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/update/<int:scenario_id>", methods=["PUT"])
def update_scenario(scenario_id):
    data = request.json
    name = data.get("name")
    description = data.get("description")

    if name is not None and not isinstance(name, str):
        return jsonify({"error": "Name must be a string."}), 400
    if description is not None and not isinstance(description, str):
        return jsonify({"error": "Description must be a string."}), 400

    try:
        updated = scenario_service.update(db.session, scenario_id, name=name, description=description)
        return jsonify({"success": True, "scenario": updated}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/delete/<int:scenario_id>", methods=["DELETE"])
def delete_scenario(scenario_id):
    try:
        result = scenario_service.delete(db.session, scenario_id)
        return jsonify({"success": True, "message": result["message"]}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
