import streamlit as st
import streamlit_authenticator as stauth
import requests
from config import API_URL

@st.cache_data(ttl=300)
def carregar_usuarios_da_api():
  response = requests.get(f"{API_URL}users/")
  data = response.json()
  if not data["success"]:
    raise Exception("Erro na API: 'success' é False.")
  usuarios = data["users"]
  credentials = {"usernames": {}}
  for u in usuarios:
    credentials["usernames"][u["email"]] = {
      "name": u["name"],
      "password": u["password_hash"]
    }
  usuarios_por_email = {u["email"]: u for u in usuarios}
  return credentials, usuarios_por_email

def get_authenticator():
  credentials, usuarios_por_email = carregar_usuarios_da_api()
  authenticator = stauth.Authenticate(
    credentials,
    cookie_name="auth_cookie",
    key="signature_key",
    cookie_expiry_days=1
  )
  return authenticator, usuarios_por_email


def require_login():
  if st.session_state.get("authentication_status") != True:
    st.warning("⚠️ Você precisa estar logado para acessar esta página.")
    st.stop()