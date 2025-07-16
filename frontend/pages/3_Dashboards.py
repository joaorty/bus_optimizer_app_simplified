import streamlit as st
from utils import get_authenticator, carregar_cenarios, Navbar, gerar_dashboard, Icon

Icon()
Navbar()
authenticator, usuarios_por_email = get_authenticator()

if st.session_state.get("authentication_status"):
  user_id = usuarios_por_email[st.session_state["username"]]["id"]
  st.session_state["user_id"] = user_id
else:
  st.warning("⚠️ Você precisa estar logado para acessar esta página.")
  st.stop()


st.title("📊 Dashboards dos Cenários")

cenarios = carregar_cenarios(user_id=st.session_state.get("user_id"))

if not cenarios:
  st.warning("Você ainda não criou nenhum cenário.")
  st.markdown("👉 [Clique aqui para criar um novo cenário](./Criar_e_Otimizar)")
  st.stop()

nomes_cenarios = [ cenario.get( "name" ) for cenario in cenarios ]

cenario_selecionado = st.selectbox("Selecione um cenário", nomes_cenarios)

if st.button("Gerar Dashboard"):
  try:
    indice = nomes_cenarios.index(cenario_selecionado)
    dados_cenario = cenarios[indice]
    figs = gerar_dashboard(dados_cenario)  # lista de figuras

    # Criar abas para separar gráficos
    tabs = st.tabs([
      "Demanda & Rotas",
      "Tipos de Ônibus",
      "Solução & Headway",
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

  except Exception as e:
    st.error(f"Erro ao gerar dashboard: {e}")
