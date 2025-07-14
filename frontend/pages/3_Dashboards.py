import streamlit as st
from modules.auth import require_login
from modules.carregar_cenarios import carregar_cenarios
from modules.nav import Navbar
from modules.dashboard import gerar_dashboard

Navbar()
require_login()

st.title("📊 Dashboards dos Cenários")

cenarios = carregar_cenarios()
nomes_cenarios = list(cenarios.keys())

if not nomes_cenarios:
  st.warning("⚠️ Nenhum cenário disponível.")
  st.stop()

cenario_selecionado = st.selectbox("Selecione um cenário", nomes_cenarios)

if st.button("Gerar Dashboard"):
  try:
    dados_cenario = cenarios[cenario_selecionado]
    figs = gerar_dashboard(dados_cenario)  # lista de figuras

    # Criar abas para separar gráficos
    tabs = st.tabs([
      "Demanda & Rotas",
      "Tipos de Ônibus",
      "Solução & Headway",
      "Parâmetros & Objetivo"
    ])

    # 1. Demanda & Rotas
    with tabs[0]:
      if len(figs) > 0:
        st.plotly_chart(figs[0], use_container_width=True)
      else:
        st.info("Sem dados de demanda por rota.")

    # 2. Tipos de Ônibus
    with tabs[1]:
      if len(figs) > 1:
        st.plotly_chart(figs[1], use_container_width=True)
      else:
        st.info("Sem dados de tipos de ônibus.")

    # 3. Solução & Headway
    with tabs[2]:
      if len(figs) > 2:
        # Colunas lado a lado para dois gráficos
        col1, col2 = st.columns(2)
        col1.plotly_chart(figs[2], use_container_width=True)
        if len(figs) > 3:
          col2.plotly_chart(figs[3], use_container_width=True)
        else:
          col2.info("Sem dados de headway.")
      else:
        st.info("Sem dados da solução otimizada.")

    # 4. Parâmetros & Objetivo
    with tabs[3]:
      # Exibe métricas e parâmetros (essas partes devem estar sendo renderizadas dentro do gerar_dashboard)
      # Se não, pode retornar separadamente e exibir aqui
      parametros = dados_cenario.get("parameters", [])
      if parametros:
        st.subheader("⚙️ Parâmetros do Modelo")
        st.json(parametros[0])
      else:
        st.info("Sem parâmetros disponíveis.")

      solutions = dados_cenario.get("solutions", [])
      if solutions and solutions[0].get("objective_value") is not None:
        st.metric("🎯 Valor Objetivo da Solução", round(solutions[0]["objective_value"], 2))
      else:
        st.info("Sem valor objetivo disponível.")

  except Exception as e:
    st.error(f"Erro ao gerar dashboard: {e}")
