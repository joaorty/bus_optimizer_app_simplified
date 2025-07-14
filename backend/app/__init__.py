import os
from app.utils import DatabaseSQLAlchemy

from flask import Flask, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

from .controllers import register_routes
from .models import *

db = DatabaseSQLAlchemy.get_db(  )
migrate = Migrate(  )

def create_app( test_config = None ):
    templates_path = 'Views/templates'
    static_path = 'Views/static'

    app = Flask(
        __name__,
        instance_relative_config = True,
        template_folder = templates_path,
        static_folder = static_path
    )

    app.config.from_prefixed_env(  )

    if test_config is None:
        app.config.from_object( Config )
    else:
        app.config.from_mapping( test_config )
    
    try:
        os.makedirs( app.instance_path )
    except OSError:
        pass

    CORS(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:3000"],  # Frontend React
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Accept", "Access-Control-Allow-Headers",  "X-Requested-With"],
                "supports_credentials": True,
                "expose_headers": ["Content-Range", "X-Content-Range"],
            }
        },
        supports_credentials=True,
    )

    DatabaseSQLAlchemy.init_app( app )
    migrate.init_app( app, db )

    with app.app_context(  ):
        db.create_all(  )

    register_routes( app )

    return app