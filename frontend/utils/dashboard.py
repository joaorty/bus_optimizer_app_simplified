import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def gerar_dashboard(cenario: dict):
  figs = []

  # --- 1. Rotas: demanda por rota ---
  rotas = cenario.get("routes", [])
  if rotas:
    df_rotas = pd.DataFrame(rotas)
    fig1 = px.bar(
      df_rotas,
      x="id",
      y="passengers",
      title="Demanda de Passageiros por Rota",
      labels={"id": "Rota", "passengers": "Passageiros"}
    )
    figs.append(fig1)

  # --- 2. Tipos de ônibus: custo e capacidade ---
  bus_types = cenario.get("bus_types", [])
  if bus_types:
    df_buses = pd.DataFrame(bus_types)
    fig2 = px.bar(
      df_buses,
      x="id",
      y=["seat_capacity", "available_units"],
      barmode="group",
      title="Capacidade e Unidades Disponíveis por Tipo de Ônibus",
      labels={"id": "Tipo de Ônibus"}
    )
    figs.append(fig2)

  # --- 3. Solução otimizada: uso de ônibus por tipo ---
  solution = cenario.get("solution", {})
  
  if solution:
    sol = solution
    v_dict = sol["solution_data"]["variables"]["v"]  # Ex: {"1_3": 2, ...}
    v_df = pd.DataFrame([
      {"bus_id": int(k.split("_")[0]), "route_id": int(k.split("_")[1]), "value": v}
      for k, v in v_dict.items()
    ])
    fig3 = px.bar(
      v_df,
      x="bus_id",
      y="value",
      color="route_id",
      title="Uso dos Ônibus por Tipo e Rota",
      labels={"bus_id": "Tipo de Ônibus", "value": "Unidades Usadas"}
    )
    figs.append(fig3)

    # --- 4. Headway por rota ---
    h_dict = sol["solution_data"]["variables"]["H"]
    h_df = pd.DataFrame([
      {"route_id": int(r), "headway": h}
      for r, h in h_dict.items()
    ])
    fig4 = px.bar(
      h_df,
      x="route_id",
      y="headway",
      title="Headway por Rota",
      labels={"route_id": "Rota", "headway": "Minutos"}
    )
    figs.append(fig4)

    # --- 5. Valor objetivo ---
    st.metric(label="🎯 Valor Objetivo da Solução", value=round(sol["objective_value"], 2))

    # --- 6. Parâmetros utilizados ---
    parametros = cenario.get("parameters", [])
    if parametros:
      st.subheader("⚙️ Parâmetros do Modelo")
      st.json(parametros[0])  # mostra primeiro conjunto

  else:
    st.warning("⚠️ Nenhuma solução otimizada encontrada para este cenário.")

  return figs
