import streamlit as st


def Navbar():
    with st.sidebar:
        st.page_link('app.py', label='Início', icon='🏠')
        st.page_link('pages/0_Login.py', label='Login', icon='🔐')
        st.page_link('pages/1_Criar_e_Otimizar.py', label='Criação e Otimização de Cenários', icon='🔧')
        st.page_link('pages/2_Cenarios_Otimizados.py', label='Gerenciar Cenários Otimizados', icon='📁')
        st.page_link('pages/3_Dashboards.py', label='Visualizar Dashboards', icon='📊')