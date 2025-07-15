import requests
import streamlit as st
from config import API_URL

def carregar_cenarios(user_id):
    """Consulta a API Flask e retorna os cenários disponíveis."""
    try:
        response = requests.get(f"{API_URL}scenarios/get_all", params={"user_id": user_id})
        data = response.json()

        if not data["success"]:
            raise Exception("Erro na API: 'success' é False.")

        return data["cenarios"]

    except Exception as e:
        st.error(f"⚠️ Erro ao carregar cenários da API Flask: {e}")
        st.stop()
