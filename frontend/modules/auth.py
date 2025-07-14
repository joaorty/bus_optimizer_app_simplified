import streamlit as st

def require_login():
  if st.session_state.get("authentication_status") != True:
    st.warning("⚠️ Você precisa estar logado para acessar esta página.")
    st.stop()