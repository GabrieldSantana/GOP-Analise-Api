import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def run_dashboard_casos():
    st.title("Dashboard de Distribuição de Casos")

    
    with st.sidebar:
        st.header("Filtros")
        status = st.selectbox("Status do caso", options=["", "Em andamento", "Fechado", "Outro"], index=0)
        data_inicio = st.date_input("Data início", value=None)
        data_fim = st.date_input("Data fim", value=None)

    params = {}
    if status:
        params['status'] = status
    if data_inicio:
        params['data_inicio'] = data_inicio.strftime("%Y-%m-%d")
    if data_fim:
        params['data_fim'] = data_fim.strftime("%Y-%m-%d")

    url = "https://gop-analise-api.onrender.com/api/dashboard/casos"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        casos = data.get("data", [])
        aggs = data.get("aggregations", {})

        st.markdown(f"### Total de casos retornados: {len(casos)}")

      
        local_count = aggs.get("local_count", {})
        if local_count:
            fig_local = px.bar(
                x=list(local_count.keys()),
                y=list(local_count.values()),
                title="Casos por Local",
                labels={"x": "Local", "y": "Quantidade"},
                color=list(local_count.keys()),
                color_discrete_sequence=px.colors.qualitative.Pastel,
                orientation='v'  
            )
            st.plotly_chart(fig_local)

      
        status_count = aggs.get("status_count", {})
        if status_count:
            fig_status = px.pie(
                names=list(status_count.keys()),
                values=list(status_count.values()),
                title="Distribuição por Status",
                hole=0.3
            )
            st.plotly_chart(fig_status)

      
        data_count = aggs.get("data_count", {})
        if data_count:
            meses = list(data_count.keys())
            valores = list(data_count.values())
            fig_data = px.line(
                x=meses,
                y=valores,
                title="Distribuição Mensal de Casos",
                labels={"x": "Mês", "y": "Quantidade"},
                markers=True
            )
            st.plotly_chart(fig_data)

    
        if local_count:
            fig_local_donut = go.Figure(data=[go.Pie(
                labels=list(local_count.keys()),
                values=list(local_count.values()),
                hole=0.5,
                hoverinfo="label+percent+value",
                textinfo="percent"
            )])
            fig_local_donut.update_layout(title_text="Distribuição por Local (Donut)")
            st.plotly_chart(fig_local_donut)

    else:
        st.error("Erro ao buscar dados do servidor.")
