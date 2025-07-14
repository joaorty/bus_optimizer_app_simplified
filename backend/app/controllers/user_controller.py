from flask import Blueprint, request, jsonify
from app.services import UserService

bp = Blueprint("user", __name__, url_prefix="/api/users")
user_service = UserService()

@bp.route("/", methods=["GET"])
def get_all_users():
    try:
        users = user_service.get_all_users()
        return jsonify({"success": True, "users": users}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = user_service.get_user_by_id(user_id)
        return jsonify({"success": True, "user": user}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/username/<string:username>", methods=["GET"])
def get_user_by_username(username):
    try:
        user = user_service.get_user_by_username(username)
        return jsonify({"success": True, "user": user}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id):
    data = request.get_json()
    new_username = data.get("username")
    new_password = data.get("password")

    if not new_username or not new_password:
        return jsonify({"error": "Both username and password are required."}), 400

    try:
        updated_user = user_service.update_user_by_id(user_id, new_username, new_password)
        return jsonify({"success": True, "user": updated_user}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/username/<string:old_username>", methods=["PUT"])
def update_user_by_username(old_username):
    data = request.get_json()
    new_username = data.get("username")
    new_password = data.get("password")

    if not new_username or not new_password:
        return jsonify({"error": "Both new username and password are required."}), 400

    try:
        updated_user = user_service.update_user_by_username(old_username, new_username, new_password)
        return jsonify({"success": True, "user": updated_user}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    try:
        deleted_user = user_service.delete_user_by_id(user_id)
        return jsonify({"success": True, "deleted_user": deleted_user}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/username/<string:username>", methods=["DELETE"])
def delete_user_by_username(username):
    try:
        deleted_user = user_service.delete_user_by_username(username)
        return jsonify({"success": True, "deleted_user": deleted_user}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/<int:user_id>/simulations", methods=["GET"])
def get_user_simulations(user_id):
    try:
        simulations = user_service.get_user_simulations(user_id)
        return jsonify({"success": True, "simulations": simulations}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


@bp.route("/<int:user_id>/parameters", methods=["GET"])
def get_user_parameters(user_id):
    try:
        parameters = user_service.get_user_parameters(user_id)
        return jsonify({"success": True, "parameters": parameters}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
