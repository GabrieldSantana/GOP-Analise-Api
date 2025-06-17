import requests
import streamlit as st
import plotly.express as px

def run_dashboard_evidencias():
    st.title("Dashboard de Evidências por Caso")

  
    with st.sidebar:
        st.header("Filtros")
        caso_id = st.text_input("ID do Caso (opcional)")
        tipo_evidencia = st.text_input("Tipo de Evidência (opcional)")

    params = {}
    if caso_id:
        params['caso_id'] = caso_id
    if tipo_evidencia:
        params['tipo_evidencia'] = tipo_evidencia

    url = "https://gop-analise-api.onrender.com/api/dashboard/evidencias"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        aggs = data.get("aggregations", {})
        evidencias_por_caso = aggs.get("evidencias_por_caso", {})

        if evidencias_por_caso:
            st.markdown(f"### Total de casos com evidências: {len(evidencias_por_caso)}")

     
            fig = px.bar(
                x=list(evidencias_por_caso.keys()),
                y=list(evidencias_por_caso.values()),
                title="Número de Evidências por Caso",
                labels={"x": "Caso", "y": "Quantidade de Evidências"},
                color=list(evidencias_por_caso.keys()),
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig)

        else:
            st.info("Nenhuma evidência encontrada com os filtros aplicados.")

    else:
        st.error(f"Erro ao buscar dados do servidor. Status code: {response.status_code}")
