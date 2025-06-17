import streamlit as st
import pandas as pd
import requests

from dashboard.dashboard_peritos import run_dashboard_peritos
from dashboard.dashboard_vitimas import run_dashboard_vitimas
from dashboard.dashboard_casos import run_dashboard_casos
from dashboard.dashboard_evidencias import run_dashboard_evidencias
from dashboard.dashboard_coeficientes import run_dashboard_coeficientes

from modelo_ml.modelos_dashboard import executar_modelo_regressao, executar_modelo_kmeans


def carregar_dados_vitimas():
    url = "https://gop-analise-api.onrender.com/api/dashboard/vitimas"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return pd.DataFrame(json_data.get("data", []))
        else:
            st.error("Erro ao carregar dados de vítimas.")
    except Exception as e:
        st.error(f"Erro na requisição de vítimas: {e}")
    return pd.DataFrame()


def carregar_dados_peritos():
    url = "https://gop-analise-api.onrender.com/api/dashboard/peritos"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            casos_por_perito = json_data.get("casos_por_perito", {})
            return pd.DataFrame(list(casos_por_perito.items()), columns=["Perito", "Casos"])
        else:
            st.error("Erro ao carregar dados dos peritos.")
    except Exception as e:
        st.error(f"Erro na requisição de peritos: {e}")
    return pd.DataFrame()



def main():
    st.set_page_config(page_title="Dashboard de Análise Criminal", layout="wide")
    st.sidebar.title("Menu")

    option = st.sidebar.selectbox(
        "Escolha o dashboard", 
        (
            "Casos por Perito", 
            "Estatísticas de Vítimas", 
            "Distribuição de Casos", 
            "Evidências", 
            "Coeficientes",
            "Modelos de Machine Learning"
        )
    )

    if option == "Casos por Perito":
        run_dashboard_peritos()

    elif option == "Estatísticas de Vítimas":
        run_dashboard_vitimas()

    elif option == "Distribuição de Casos":
        run_dashboard_casos()

    elif option == "Evidências":
        run_dashboard_evidencias()

    elif option == "Coeficientes":
        run_dashboard_coeficientes()

    elif option == "Modelos de Machine Learning":
        st.title("Modelos de Machine Learning")

        
        df_vitimas = carregar_dados_vitimas()
        if df_vitimas.empty:
            st.warning("Dados de vítimas vazios.")
        else:
            executar_modelo_regressao(df_vitimas)

    
        df_peritos = carregar_dados_peritos()
        if not df_peritos.empty and "Casos" in df_peritos.columns:
            executar_modelo_kmeans(df_peritos)
        else:
            st.warning("Dados de peritos insuficientes ou mal formatados para clusterização.")


if __name__ == "__main__":
    main()
