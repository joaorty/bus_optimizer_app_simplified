from flask import Blueprint, jsonify, request
from app.services.scenario_service import ScenarioService

bp = Blueprint("scenario", __name__, url_prefix="/api/scenarios")
scenario_service = ScenarioService()

@bp.route("/create", methods=["POST"])
def create_scenario():
    data = request.json
    user_id = data.get("user_id")
    name = data.get("name")
    description = data.get("description")
    list_routes = data.get("routes", [])
    bus_types = data.get("bus_types", [])
    parameters = data.get("parameters", {})

    try:
        scenario = scenario_service.create(user_id=user_id, name=name, description=description)
        return jsonify({"success": True, "scenario": scenario}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/get/<int:scenario_id>", methods=["GET"])
def get_scenario(scenario_id):
    user_id = request.args.get("user_id", type=int)

    try:
        scenario = scenario_service.get_by_id(user_id=user_id, scenario_id=scenario_id)
        return jsonify({"success": True, "scenario": scenario}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/get_all", methods=["GET"])
def get_all_scenarios():
    user_id = request.args.get("user_id", type=int)

    try:
        scenarios = scenario_service.get_all(user_id=user_id)
        return jsonify({"success": True, "cenarios": scenarios}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/update/<int:scenario_id>", methods=["PUT"])
def update_scenario(scenario_id):
    data = request.json
    user_id = data.get("user_id")
    name = data.get("name")
    description = data.get("description")

    try:
        updated = scenario_service.update(user_id=user_id, scenario_id=scenario_id, name=name, description=description)
        return jsonify({"success": True, "scenario": updated}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/delete/<int:scenario_id>", methods=["DELETE"])
def delete_scenario(scenario_id):
    user_id = request.args.get("user_id", type=int)

    try:
        result = scenario_service.delete(user_id=user_id, scenario_id=scenario_id)
        return jsonify({"success": True, "message": result["message"]}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
