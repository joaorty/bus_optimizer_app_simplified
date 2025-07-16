import plotly.express as px
import pandas as pd
import streamlit as st

def gerar_dashboard(cenario: dict):
  figs = []

  # --- 1. Demanda por Rota ---
  rotas = cenario.get("routes", [])
  if rotas:
    df_rotas = pd.DataFrame(rotas)
    fig1 = px.bar(
      df_rotas,
      x="id",
      y="passengers",
      title="📍 Demanda de Passageiros por Rota",
      labels={"id": "Rota", "passengers": "Passageiros"}
    )
    figs.append(fig1)

  # --- 2. Capacidade e Frota dos Ônibus ---
  bus_types = cenario.get("bus_types", [])
  if bus_types:
    df_buses = pd.DataFrame(bus_types)
    fig2 = px.bar(
      df_buses,
      x="id",
      y=["seat_capacity", "available_units"],
      barmode="group",
      title="🚌 Capacidade e Frota por Tipo de Ônibus",
      labels={"id": "Tipo de Ônibus", "seat_capacity": "Capacidade de Assentos", "available_units": "Unidades Disponíveis"}
    )
    figs.append(fig2)

  # --- 3. Solução Otimizada ---
  solution = cenario.get("solution", {})
  if solution:
    sol_data = solution["solution_data"]["variables"]

    # Uso de ônibus por tipo e rota
    v_dict = sol_data.get("v", {})
    if v_dict:
      v_df = pd.DataFrame([
        {"Tipo de Ônibus": int(k.split("_")[0]), "Rota": int(k.split("_")[1]), "Unidades Usadas": v}
        for k, v in v_dict.items()
      ])
      fig3 = px.bar(
        v_df,
        x="Tipo de Ônibus",
        y="Unidades Usadas",
        color="Rota",
        title="🚌 Alocação de Ônibus por Tipo e Rota"
      )
      figs.append(fig3)

    # Headway por rota
    h_dict = sol_data.get("H", {})
    if h_dict:
      h_df = pd.DataFrame([
        {"Rota": int(r), "Headway (min)": h}
        for r, h in h_dict.items()
      ])
      fig4 = px.bar(
        h_df,
        x="Rota",
        y="Headway (min)",
        title="⏱️ Intervalo Médio (Headway) por Rota"
      )
      figs.append(fig4)

    # Valor Objetivo da Solução
    objetivo = solution.get("objective_value")
    if objetivo is not None:
      st.metric(label="🎯 Custo Total da Solução", value=f"R$ {round(objetivo, 2):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Parâmetros do Modelo
    parametros = cenario.get("parameters", [])
    if parametros:
      st.subheader("⚙️ Parâmetros do Modelo")
      param = parametros[0]
      col1, col2 = st.columns(2)

      col1.markdown(f"**⏱️ Período Total:** {param.get('units_time')} min")
      col1.markdown(f"**🔁 Tempo Máx. Transferência:** {param.get('acceptable_time_transfer')} min")

      col2.markdown(f"**⏳ Custo de Espera:** R$ {param.get('wait_cost'):.2f}")
      col2.markdown(f"**👥 Custo de Aglomeração:** R$ {param.get('agglomeration_cost'):.2f}")

  else:
    st.warning("⚠️ Nenhuma solução otimizada encontrada para este cenário.")

  return figs
