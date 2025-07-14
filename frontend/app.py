import streamlit as st
from modules.nav import Navbar

def main():
  Navbar()

  st.title(f'🚌 Sistema de Alocação de Ônibus')
  st.markdown("Navegue usando o menu à esquerda para:")
  st.markdown("- Criar e otimizar novos cenários")
  st.markdown("- Visualizar cenários otimizados")
  st.markdown("- Acessar dashboards com métricas")

  st.info("Use o menu lateral para acessar as funcionalidades.")


if __name__ == '__main__':
    main()
