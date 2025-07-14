from flask import (
    Blueprint, g, request, session, jsonify
)
from functools import wraps
from app.services import UserService

bp = Blueprint( "auth", __name__, url_prefix = "/api/auth" )

def login_required( view ):
    @wraps( view )
    def wrapped_view( **kwargs ):
        if g.user is None:
            return jsonify({ "error" : f"You must be logged in to do this action." })
        return view( **kwargs )
    
    return wrapped_view

@bp.before_app_request
def load_logged_in_user(  ):
    user_id = session.get( "user_id" )

    if user_id is None:
        g.user = None
    else:
        user_service = UserService(  )
        g.user = user_service.get_user_by_id( user_id )

@bp.route( "/register", methods = [ "POST" ] )
def register(  ):
    data = request.get_json(  )
    name     = data.get( "name" )
    username = data.get( "username" )
    password = data.get( "password" )

    user_service = UserService(  )
    try:
        new_user = user_service.create_user( name, username, password )
        return jsonify({
            "success" : True,
            "message" : "PortUser created successfully",
            "user"    : new_user
        }), 201
    except ValueError as e:
        return jsonify( { "error" : f"{ str( e ) }" } ), 400
    except Exception as e:
        return jsonify( { "error" : f"Internal error in the server - { str( e ) }" } ), 500

@bp.route( "/login", methods = [ "POST" ] )
def login(  ):
    try:
        data = request.get_json(  )
        if not data:
            return jsonify({"error": "Corpo da requisição vazio"}), 400
        
        username = data.get( "username" )
        password = data.get( "password" )

        user_service = UserService(  )
        logged_user = user_service.login( username, password )
        print( logged_user )
        session.clear(  )
        session[ "user_id" ] = logged_user[ "id" ]

        return jsonify( {
            "success" : True,
            "message" : "PortUser logged in successfully",
            "user" : logged_user
        } ), 200
    except ValueError as e:
        print( e )
        return jsonify( { "error" : str( e ) } ), 400
    except Exception as e:
        print( e )
        return jsonify( { "error" : f"Internal error in the server - { str( e ) }" } ), 500

@bp.route( "/logout", methods = [ "POST" ] )
def logout(  ):
    user = g.user
    session.clear(  )
    return jsonify({
        "success"   : True,
        "message"   : "Used logged out successfully",
        "user" : user
    }), 200