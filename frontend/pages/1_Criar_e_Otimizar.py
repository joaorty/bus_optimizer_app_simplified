import streamlit as st
import pandas as pd
import requests
from utils import Navbar, require_login, Icon
from config import API_URL

Icon()
Navbar()
require_login()

st.title("🔧 Criar e Otimizar Cenário")

name_scenario = st.text_input("Nome do cenário")

st.write("Preencha os detalhes do cenário:")

num_types = st.number_input("Quantos tipos de ônibus existem?", min_value=1, step=1)

bus_types = []
for i in range(num_types):
  with st.expander(f"Tipo de ônibus {i+1}"):
    tipo = {
      "operational_cost": st.number_input("Custo operacional por km (R$)", min_value=0.0, value=1.0, key=f"custo_{i}"),
      "capacity": st.number_input("Quantidade de assentos", min_value=1, value=50, step=50, key=f"assentos_{i}"),
      "available_units": st.number_input("Quantidade de ônibus disponíveis", min_value=0, value=10, step=10, key=f"qtd_{i}"),
      "load_factor": st.number_input("Fator máximo de ocupação", min_value=1.0, value=1.0, step=0.1, key=f"fator_{i}")
    }
    bus_types.append(tipo)

num_routes = st.number_input("Quantas rotas existem?", min_value=1, step=1)
routes = []
for i in range(num_routes):
  with st.expander(f"Rota {i+1}"):
    route = {
      "length_km": st.number_input("Comprimento da rota (km)", min_value=0.50, step=0.50,key=f"comprimento_{i}"),
      "time_minutes": st.number_input("Tempo de viagem (minutos)", min_value=1, key=f"tempo_{i}"),
      "passengers": st.number_input("Número de passageiros", min_value=1, value=50, step=50, key=f"passageiros_{i}")
    }
    routes.append(route)

# Sobre os parametros
parameters = dict()
parameters["time_unit_of_periods"] = st.number_input("Tempo do período (minutos)", min_value=0, value=60, step=1)
parameters["accetable_time_transfer"] = st.number_input("Tempo aceitável de transferência (minutos)", min_value=0, step=1)
parameters["agglomeration_cost"] = st.number_input("Custo de aglomeração", min_value=0.0, value=1.0, step=0.5)
parameters["wait_cost"] = st.number_input("Custo de tempo de espera", min_value=0.0, value=1.0, step=0.5)

if st.button("Otimizar"):
  print({
      "name_scenario": name_scenario,
      "bus_types": bus_types,
      "routes": routes,
      "parameters": parameters,
      "mode": "manual",
      "user_id": st.session_state.get("user_id"),
    })
  response = requests.post(
    API_URL + "solver/run-static-model",
    json={
      "name_scenario": name_scenario,
      "bus_types": bus_types,
      "routes": routes,
      "parameters": parameters,
      "mode": "manual",
      "user_id": st.session_state.get("user_id"),
    }
  )
  if response.ok:
    st.success("Cenário enviado para otimização com sucesso!")
    st.json(response.json())
  else:
    st.error(f"Erro {response.status_code} ao enviar cenário para otimização.")
    
    # Tenta exibir o JSON se possível
    try:
      st.json(response.json())
    except Exception:
      st.write("Resposta bruta da API:")
      st.code(response.text)