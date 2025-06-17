import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.decomposition import PCA

from modelo_ml.regression_model import train_linear_regression
from modelo_ml.clustering_model import train_kmeans
from utils.utils import remover_colunas_complexas, preprocessar_dados_para_regressao


def executar_modelo_regressao(df: pd.DataFrame):
    df = remover_colunas_complexas(df)
    st.subheader("Amostra dos dados das vítimas")
    st.write(df.head())

    if "idade" in df.columns:
        st.subheader("Treinando Regressão Linear para prever 'idade'")
        try:
            X, y = preprocessar_dados_para_regressao(df, target_col="idade")
            model_lr, mse = train_linear_regression(X, y)
            st.success(f"Erro Quadrático Médio (Regressão Linear): {mse:.4f}")

            y_pred = model_lr.predict(X)
            fig, ax = plt.subplots()
            ax.scatter(y, y_pred, alpha=0.6)
            ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
            ax.set_xlabel("Idade Real")
            ax.set_ylabel("Idade Predita")
            ax.set_title("Regressão Linear: Idade Real vs Predita")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erro no modelo de regressão: {e}")
    else:
        st.info("Coluna 'idade' não encontrada para regressão.")


def executar_modelo_kmeans(df: pd.DataFrame):
    st.subheader("Clusterização KMeans com Casos por Perito")
    try:
        df_cluster_input = df[["Casos"]]
        model_kmeans, df_clustered = train_kmeans(df_cluster_input, n_clusters=3)

        df_resultado = df.copy()
        df_resultado["cluster"] = df_clustered["cluster"]
        st.write(df_resultado)

        if df_cluster_input.shape[1] == 1:
            df_cluster_input["dummy"] = 0

        pca = PCA(n_components=2)
        componentes = pca.fit_transform(df_cluster_input)
        df_plot = pd.DataFrame(componentes, columns=["PC1", "PC2"])
        df_plot["Cluster"] = df_resultado["cluster"]
        df_plot["Perito"] = df_resultado["Perito"]

        fig, ax = plt.subplots()
        sns.scatterplot(x="PC1", y="PC2", hue="Cluster", data=df_plot, palette="viridis", s=100)
        for i in range(len(df_plot)):
            ax.text(df_plot["PC1"][i], df_plot["PC2"][i], df_plot["Perito"][i], fontsize=8)
        ax.set_title("Clusters de Peritos (KMeans com PCA)")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro na clusterização de peritos: {e}")
