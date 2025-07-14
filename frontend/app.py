import streamlit as st
from modules.nav import Navbar

def main():
  Navbar()

  st.title('🚌 Sistema de Alocação de Ônibus')
  st.markdown("""
  Bem-vindo ao sistema de alocação de ônibus com otimização linear.

  Use o menu à esquerda para:
  - Criar e otimizar novos cenários
  - Visualizar resultados otimizados
  - Acessar dashboards com métricas e análises

  ---
  """)

  st.info("Antes, é necessário realizar login para acessar todas as funcionalidades do sistema.")

  if st.button("Ir para Login"):
    st.switch_page("pages/0_Login.py")

  st.markdown("### 📘 Sobre o Projeto")
  st.markdown("""
  Este sistema visa alocar ônibus em diferentes rotas urbanas de forma eficiente,
  minimizando custos operacionais e maximizando o atendimento à demanda de passageiros.

  O modelo considera:
  - Diferentes tipos de ônibus e suas capacidades
  - Demandas específicas por rota
  - Custos operacionais, de espera, de aglomeração e transferência
  - Fatores como frequência, intervalo, e frota disponível
  """)

  with st.expander("🔍 Ver Modelo Matemático Explicado"):
    st.subheader("🎯 Objetivo do Modelo")
    st.markdown("""
    O modelo resolve como alocar diferentes tipos de ônibus entre diversas rotas de forma a minimizar os custos totais do sistema.
    Esses custos incluem operação, espera dos passageiros, aglomeração, transferências e demanda não atendida.
    """)

    st.subheader("📚 Conjuntos e Índices")
    st.markdown("""
    - $R$: conjunto de rotas disponíveis
    - $B$: conjunto de tipos de ônibus
    - $r \\in R$: índice para uma rota específica
    - $b \\in B$: índice para um tipo de ônibus
    - $K_r$: conjunto de possíveis frequências para a rota $r$
    
    Esses conjuntos são a base para estruturar as decisões.
    """)

    st.subheader("🔢 Parâmetros de Entrada")
    st.markdown("""
    - **$P$**: Período total considerado (em minutos).
    - **$TC_r$**: Tempo de ciclo de uma viagem completa da rota $r$.
    - **$W$**: Tempo máximo aceitável de espera.
    - **$Q_{max}^r$**: Demanda máxima estimada para a rota $r$.
    - **$CAP_b$**: Capacidade de assentos do ônibus do tipo $b$.
    - **$FC_{max}^b$**: Fator máximo de carga permitido (ex: 1.2 significa até 120% da capacidade sentada).
    - **$FT_b$**: Frota disponível do tipo $b$.
    - **$CC_r$**: Comprimento da rota $r$ (usado para calcular custo por km).
    - **$C_{ope}^b$**: Custo operacional por km do ônibus $b$.
    - **$C_{esp}$**: Custo de espera por minuto por passageiro.
    - **$C_{aglo}$**: Custo por passageiro excedente à capacidade.
    - **$C_{tran}$**: Custo por passageiro transferido.
    - **$M$**: Penalidade elevada para demanda não atendida.
    - **$\\alpha$**: Fator de segurança para definir a frequência máxima.
    """)

    st.subheader("🧩 Variáveis de Decisão")
    st.markdown("""
    - **$v_{b,r}$**: Quantidade de ônibus do tipo $b$ alocados na rota $r$.
    - **$f_{b,r}$**: Frequência de ônibus do tipo $b$ na rota $r$.
    - **$q_{b,r}$**: Passageiros transportados por ônibus $b$ na rota $r$.
    - **$y_r$**: Ativação da rota ($1$ se usada, $0$ se não).
    - **$e_{b,r}$**: Excesso de passageiros além da capacidade.
    - **$w_r$**: Passageiros que fazem transferência.
    - **$z_r$**: Passageiros que não foram atendidos.
    - **$H_r$**: Intervalo médio entre ônibus na rota $r$.
    - **$\\delta_{tot}^{k,r}$**: Binária para ativar uma frequência $k$ na rota $r$.
    """)

    st.subheader("📉 Função Objetivo")
    st.latex(r"""
    \min Z = \sum_{b \in B} \sum_{r \in R} C_{ope}^b \cdot CC_r \cdot f_{b,r}
    + \sum_{r \in R} \frac{H_r}{2} \cdot C_{esp}
    + \sum_{b \in B} \sum_{r \in R} e_{b,r} \cdot C_{aglo} \\
    + \sum_{r \in R} C_{tran} \cdot w_r
    + \sum_{r \in R} M \cdot z_r
    """)

    st.markdown("A função objetivo busca minimizar o custo total do sistema com cinco componentes principais:")
    st.markdown("""
    1. **Custo Operacional**: frequência x distância x custo por tipo.
    2. **Custo de Espera**: proporcional ao intervalo médio entre ônibus.
    3. **Custo de Aglomeração**: penaliza passageiros em pé ou excesso de lotação.
    4. **Custo de Transferência**: passageiros que precisam mudar de ônibus.
    5. **Penalidade por Demanda Não Atendida**: valor alto para forçar atendimento da população.
    """)

    st.subheader("⛓️ Restrições (Resumo)")
    st.markdown("""
    - **Frequência e Ônibus**: garante consistência entre número de ônibus e frequência usada.
    - **Tempo de Espera**: não pode ultrapassar um limite aceitável.
    - **Transferência e Aglomeração**: controlam o desconforto e riscos operacionais.
    - **Demanda**: não exceder a demanda máxima.
    - **Capacidade e Frota**: respeita limites físicos dos ônibus e da frota disponível.
    """)

    st.subheader("🔎 Interpretação da Solução")
    st.markdown("""
    Ao resolver o modelo, obtemos:
    - **$v_{b,r}^*$**: Quantos ônibus de cada tipo em cada rota.
    - **$f_{b,r}^*$**: Frequência ótima de operação.
    - **$q_{b,r}^*$**: Passageiros transportados por tipo de ônibus.
    - **$H_r^*$**: Intervalo médio final.
    - **$z_r^*$**: Demanda não atendida (idealmente zero).
    - **$e_{b,r}^*$**: Aglomeração ocorrida.

    A partir disso, podemos avaliar o desempenho do sistema com diferentes configurações e restrições.
    """)

if __name__ == '__main__':
  main()
