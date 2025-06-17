import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def run_dashboard_vitimas():
    st.title("Dashboard de Estatísticas das Vítimas")

    with st.sidebar:
        st.header("Filtros")
        etnia = st.selectbox("Etnia", options=["", "Branca", "Preta", "Parda", "Indígena", "Amarela"])
        genero = st.selectbox("Gênero", options=["", "Masculino", "Feminino", "Mulher", "Outro"])
        idade = st.slider("Idade mínima", min_value=0, max_value=100, value=0)


    if genero.lower() == "mulher":
        genero = "Feminino"

    params = {}
    if etnia:
        params['etnia'] = etnia
    if genero:
        params['genero'] = genero
    if idade > 0:
        params['idade'] = idade

    url = "https://gop-analise-api.onrender.com/api/dashboard/vitimas"
    response = requests.get(url, params=params)

    def normalizar_genero_dict(genero_count):
        mapping = {
            "feminino": "Feminino",
            "mulher": "Feminino",
            "masculino": "Masculino",
            "homem": "Masculino",
        }
        novo_contador = {}
        for k, v in genero_count.items():
            chave_norm = mapping.get(k.lower(), "Outro")
            novo_contador[chave_norm] = novo_contador.get(chave_norm, 0) + v
        return novo_contador

    if response.status_code == 200:
        data = response.json()
        aggs = data.get("aggregations", {})

        st.markdown(f"### Total de registros: {len(data.get('data', []))}")

     
        etnia_count = aggs.get("etnia_count", {})
        if etnia_count:
            fig_etnia = px.pie(
                names=list(etnia_count.keys()),
                values=list(etnia_count.values()),
                title="Distribuição por Etnia",
                hole=0
            )
            st.plotly_chart(fig_etnia)

        genero_count = aggs.get("genero_count", {})
        if genero_count:
            genero_count = normalizar_genero_dict(genero_count)
            fig_genero = px.bar(
                x=list(genero_count.keys()),
                y=list(genero_count.values()),
                title="Distribuição por Gênero",
                labels={"x": "Gênero", "y": "Quantidade"},
                color=list(genero_count.keys()),
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            st.plotly_chart(fig_genero)

       
        idade_count = aggs.get("idade_count", {})
        if idade_count:
            idades = list(idade_count.keys())
            valores = list(idade_count.values())

            fig_idade = go.Figure(data=[go.Pie(
                labels=idades,
                values=valores,
                hole=.4,
                hoverinfo="label+percent+value",
                textinfo="percent"
            )])
            fig_idade.update_layout(title_text="Distribuição por Idade (Gráfico de Rosca)")
            st.plotly_chart(fig_idade)

    else:
        st.error("Erro ao buscar dados do servidor.")
