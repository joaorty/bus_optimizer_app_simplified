import streamlit as st
from modules.auth import require_login
from modules.carregar_cenarios import carregar_cenarios
from modules.nav import Navbar

Navbar()
require_login()

st.title("📊 Dashboards dos Cenários")

cenarios = carregar_cenarios()
nomes_cenarios = list(cenarios.keys())

if not nomes_cenarios:
  st.warning("⚠️ Nenhum cenário disponível.")
  st.stop()

# Dropdown com nomes reais
cenario_selecionado = st.selectbox("Selecione um cenário", nomes_cenarios)

# Botão de geração
if st.button("Gerar Dashboard"):
  try:
    dados_cenario = cenarios[cenario_selecionado]
    fig = gerar_dashboard(dados_cenario)
    st.plotly_chart(fig, use_container_width=True)
  except Exception as e:
    st.error(f"Erro ao gerar dashboard: {e}")