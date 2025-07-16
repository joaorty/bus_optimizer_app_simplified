import streamlit as st
from utils import get_authenticator, Navbar, carregar_cenarios, Icon
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
from config import API_URL
from datetime import datetime

# Setup
Icon()
Navbar()

authenticator, usuarios_por_email = get_authenticator()

if st.session_state.get("authentication_status"):
  user_id = usuarios_por_email[st.session_state["username"]]["id"]
  st.session_state["user_id"] = user_id
else:
  st.warning("⚠️ Você precisa estar logado para acessar esta página.")
  st.stop()



st.title("📁 Cenários")
user_id = st.session_state.get("user_id")

cenarios = carregar_cenarios(user_id=user_id)

if not cenarios:
  st.warning("Você ainda não criou nenhum cenário.")
  st.markdown("👉 [Clique aqui para criar um novo cenário](./Criar_e_Otimizar)")
  st.stop()

# Criar DataFrame da tabela
cenarios_df = pd.DataFrame([
    {
        "Nome": cenario.get("name", "Sem nome"),
        "Status": cenario.get("solution", {}).get("status", "Não otimizado")
    }
    for cenario in cenarios if cenario is not None
])

# Inicializa estado
if "cenario_selecionado" not in st.session_state:
  st.session_state["cenario_selecionado"] = None
if "visualizar_cenario" not in st.session_state:
  st.session_state["visualizar_cenario"] = False

# Tabela AgGrid
st.subheader("📋 Tabela de Cenários")
gb = GridOptionsBuilder.from_dataframe(cenarios_df)
gb.configure_selection("single")
grid_options = gb.build()

response = AgGrid(
  cenarios_df,
  gridOptions=grid_options,
  update_mode=GridUpdateMode.SELECTION_CHANGED,
  fit_columns_on_grid_load=True
)

# Quando selecionar linha, atualizar estado
selected_rows = response.get("selected_rows")
if selected_rows is not None and len(selected_rows) > 0:
  nome = selected_rows.iloc[0]["Nome"]
  st.session_state["cenario_selecionado"] = nome
  st.session_state["visualizar_cenario"] = False  # reset visualização

# Se algum cenário foi selecionado
selected = st.session_state["cenario_selecionado"]
if selected:
  st.markdown(f"### 🔧 Ações para o cenário: `{selected}`")
  col1, col2 = st.columns(2)

  with col1:
    if st.button("👁️ Visualizar detalhes"):
      st.session_state["visualizar_cenario"] = True

  with col2:
    indice = next((i for i, c in enumerate(cenarios) if c.get("name") == selected), None)
    if st.button("🗑️ Excluir cenário"):
      cenario_id = cenarios[indice]["id"]
      resposta = requests.delete(f"{API_URL}scenarios/delete/{cenario_id}", json={"user_id": user_id})
      if resposta.status_code == 200:
        st.success(f"Cenário `{selected}` excluído com sucesso.")
        del cenarios[indice]
        st.session_state["cenario_selecionado"] = None
        st.session_state["visualizar_cenario"] = False
        st.rerun()
      else:
        st.error(f"Erro ao excluir cenário: {resposta.status_code} - {resposta.text}")

# Mostrar detalhes apenas se clicado em visualizar
if st.session_state["visualizar_cenario"] and selected:
  indice = next((i for i, c in enumerate(cenarios) if c.get("name") == selected), None)
  cenario = cenarios[indice]
  st.subheader("📊 Detalhes do Cenário")

  if "routes" in cenario:
    st.markdown("**🛣️ Rotas**")
    st.dataframe(pd.DataFrame(cenario["routes"]))

  if "bus_types" in cenario:
    st.markdown("**🚌 Tipos de Ônibus**")
    st.dataframe(pd.DataFrame(cenario["bus_types"]))

  if "parameters" in cenario:
    if cenario.get( "parameters" ):
      st.markdown("**⚙️ Parâmetros**")
      st.json(cenario["parameters"][0])
    else:
      st.markdown("**⚙️ Parâmetros**")
      st.json([  ])
