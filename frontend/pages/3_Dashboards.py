import streamlit as st
from utils.dashboard_tools import gerar_dashboard

from modules.nav import Navbar

Navbar()

st.title("📊 Dashboards dos Cenários")

cenario = st.selectbox("Selecione um cenário", ["cen1", "cen2"])  # depois usar o data_manager

if st.button("Gerar Dashboard"):
    fig = gerar_dashboard(cenario)
    st.plotly_chart(fig)
