import requests
import streamlit as st
import plotly.express as px

def run_dashboard_peritos():
    st.title("Casos por Perito")

    nome_perito = st.text_input("Filtrar por nome do perito (opcional):")

    params = {}
    if nome_perito:
        params['nome_perito'] = nome_perito

    url = "https://gop-analise-api.onrender.com/api/dashboard/peritos"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        casos = data.get("casos_por_perito", {})
        total = data.get("total_casos", 0)

        st.write(f"Total de casos: {total}")

        if casos:
            nomes = list(casos.keys())
            valores = list(casos.values())
            fig = px.bar(x=nomes, y=valores, labels={"x":"Perito", "y":"Número de Casos"}, title="Casos por Perito")
            st.plotly_chart(fig)
        else:
            st.write("Nenhum dado encontrado.")
    else:
        st.error("Erro ao buscar dados do servidor.")
