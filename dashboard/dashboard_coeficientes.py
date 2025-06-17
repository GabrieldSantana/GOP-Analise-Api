import streamlit as st
import requests
import plotly.express as px

def run_dashboard_coeficientes():
    st.title("Importância das Variáveis no Modelo")

    url = "https://gop-analise-api.onrender.com/api/dashboard/coefficients"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        features = data.get("features", [])
        importances = data.get("importances", [])

        if features and importances and len(features) == len(importances):
            fig = px.bar(
                x=importances,
                y=features,
                orientation='h',
                labels={"x": "Importância", "y": "Variável"},
                title="Importância das Features no Modelo",
                color=importances,
                color_continuous_scale='Blues'
            )
            fig.update_layout(yaxis=dict(autorange="reversed"))  
            st.plotly_chart(fig)
        else:
            st.warning("Dados incompletos ou inválidos retornados pela API.")
    else:
        st.error("Erro ao buscar os dados dos coeficientes.")
