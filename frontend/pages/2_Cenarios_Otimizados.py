import streamlit as st
from utils import require_login, Navbar, carregar_cenarios
import requests
from config import API_URL
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd

Navbar()
require_login()

st.title("📁 Cenários Otimizados")

cenarios = carregar_cenarios()
selected = st.selectbox("Escolha um cenário", list(cenarios.keys()))
# Monta DataFrame dos cenários
cenarios_df = pd.DataFrame([
    {
        "Nome": nome,
        "Status": cenario.get("status", "Desconhecido"),
        "Visualizar": "Visualizar",
        "Excluir": "Excluir"
    }
    for nome, cenario in cenarios.items()
])

# Configura AgGrid
gb = GridOptionsBuilder.from_dataframe(cenarios_df)
gb.configure_column("Visualizar", editable=False, cellRenderer='buttonRenderer')
gb.configure_column("Excluir", editable=False, cellRenderer='buttonRenderer')
gb.configure_selection('single')
grid_options = gb.build()

# Função customizada para botões
def button_renderer(params):
    return f'<button>{params.value}</button>'

# Exibe tabela interativa
response = AgGrid(
    cenarios_df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    allow_unsafe_jscode=True,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=False
)

# Lida com ações dos botões
if response['selected_rows']:
    selected_row = response['selected_rows'][0]
    selected = selected_row['Nome']

    # Botão Visualizar
    if st.button(f"Visualizar '{selected}'"):
        cenario = cenarios[selected]
        # Tabela de rotas
        if "rotas" in cenario:
            st.subheader("Rotas")
            st.dataframe(pd.DataFrame(cenario["rotas"]))
        # Tabela de tipos de ônibus
        if "tipos_onibus" in cenario:
            st.subheader("Tipos de Ônibus")
            st.dataframe(pd.DataFrame(cenario["tipos_onibus"]))
        # Parâmetros
        if "parametros" in cenario:
            st.subheader("Parâmetros")
            st.json(cenario["parametros"])

    # Botão Excluir
    if st.button(f"Excluir '{selected}'"):
        del cenarios[selected]
        st.success(f"Cenário '{selected}' excluído.")
        # Aqui você pode salvar novamente os cenários se necessário
if selected:
    st.subheader(f"Cenário: {selected}")
    st.json(cenarios[selected])