from dotenv import load_dotenv
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Lê variáveis do ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Monta a URL do banco
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class Config:
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = 'dev'
    
    # Configurações do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = DB_URL

    DEVELOPMENT = True
    DEBUG = True
    CSRF_ENABLED = True