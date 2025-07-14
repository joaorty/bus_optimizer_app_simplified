import streamlit as st

from modules.nav import Navbar

Navbar()

st.title("📁 Cenários Otimizados")

cenarios = carregar_cenarios()
selected = st.selectbox("Escolha um cenário", list(cenarios.keys()))

if selected:
    st.subheader(f"Cenário: {selected}")
    st.json(cenarios[selected])