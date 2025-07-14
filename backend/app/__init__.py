from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
import os
import bcrypt
from app.utils import DatabaseSQLAlchemy  # vai modificar para expor o objeto SQLAlchemy direto
from .config import Config
from .controllers import register_routes
from .models import *

# 1. Aqui, crie o objeto SQLAlchemy (não chame get_db que retorna session context manager)
db = DatabaseSQLAlchemy.get_db()  # método novo para pegar objeto SQLAlchemy
migrate = Migrate()

def create_app(test_config=None):
    global db

    templates_path = 'Views/templates'
    static_path = 'Views/static'

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=templates_path,
        static_folder=static_path
    )

    app.config.from_prefixed_env()

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:8501", "*"],  # Frontend React
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Accept", "Access-Control-Allow-Headers",  "X-Requested-With"],
                "supports_credentials": True,
                "expose_headers": ["Content-Range", "X-Content-Range"],
            }
        },
        supports_credentials=True,
    )

    # 2. Inicialize o SQLAlchemy com o app  # método novo para pegar objeto SQLAlchemy
    DatabaseSQLAlchemy.init_app(app)
    migrate.init_app(app, db)

    # 3. Crie as tabelas dentro do app context
    with app.app_context():
        db.create_all()
        
        exists = db.session.query(SolverUser).filter_by(email="admin@example.com").first()
        if not exists:
            password_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
            user = SolverUser(name="Admin", email="admin@example.com", password_hash=password_hash)
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

    register_routes(app)

    return app
