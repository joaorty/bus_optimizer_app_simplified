import streamlit as st
import streamlit_authenticator as stauth
import requests
from utils import Navbar
from config import API_URL

@st.cache_data(ttl=300)
def carregar_usuarios_da_api():
  """Consulta a API Flask e monta as credenciais para o streamlit-authenticator"""
  try:
    response = requests.get(f"{API_URL}/users/")
    data = response.json()

    if not data["success"]:
      raise Exception("Erro na API: 'success' é False.")

    usuarios = data["users"]
    credentials = {
      "usernames": {}
    }

    for u in usuarios:
      credentials["usernames"][u["email"]] = {
        "name": u["name"],
        "password": u["password"]  # Já é hash bcrypt
      }

    return credentials

  except Exception as e:
    st.error(f"⚠️ Erro ao carregar usuários da API Flask: {e}")
    st.stop()

credentials = carregar_usuarios_da_api()

authenticator = stauth.Authenticate(
  credentials,
  cookie_name="auth_cookie",
  key="signature_key",
  cookie_expiry_days=1
)

nome, auth_status, email = authenticator.login("Login", "main")

Navbar()

if auth_status is None:
  st.info("Digite seu e-mail e senha para acessar o sistema.")
  st.stop()
elif auth_status is False:
  st.error("E-mail ou senha incorretos.")
  st.stop()
elif auth_status is True:
  st.sidebar.success(f"✅ Bem-vindo, {nome}")
  authenticator.logout("Sair", "sidebar")

  # Aqui começa a área protegida
  st.success(f"Você está logado como **{email}**.")