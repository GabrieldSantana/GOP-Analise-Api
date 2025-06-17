import requests
import streamlit as st
import plotly.express as px
import pandas as pd

def run_dashboard_peritos():
    st.title("Casos por Perito")

    url = "https://gop-analise-api.onrender.com/api/dashboard/peritos"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        casos = data.get("casos_por_perito", {})
        total = data.get("total_casos", 0)

        st.write(f"Total de casos: {total}")

        if casos:
            nomes = list(casos.keys())
            valores = list(casos.values())

            # Criação do DataFrame
            df = pd.DataFrame({
                "Perito": nomes,
                "Número de Casos": valores
            })

            # Filtro na barra lateral
            perito_selecionado = st.sidebar.selectbox(
                "Filtrar por nome do perito:",
                options=["Todos"] + nomes,
                index=0
            )

            if perito_selecionado != "Todos":
                df = df[df["Perito"] == perito_selecionado]

            # Gráfico com cores distintas
            fig = px.bar(
                df,
                x="Perito",
                y="Número de Casos",
                color="Perito",
                title="Casos por Perito"
            )
            st.plotly_chart(fig)
        else:
            st.write("Nenhum dado encontrado.")
    else:
        st.error("Erro ao buscar dados do servidor.")
