import pandas as pd
import streamlit as st

def remover_colunas_complexas(df: pd.DataFrame) -> pd.DataFrame:
    cols_para_remover = []
    for col in df.columns:
        sample = df[col].dropna().head(10).tolist()
        if any(isinstance(x, (dict, list)) for x in sample):
            cols_para_remover.append(col)
    if cols_para_remover:

        df = df.drop(columns=cols_para_remover)
    return df


def preprocessar_dados_para_regressao(df: pd.DataFrame, target_col: str):
    df = df.dropna(subset=[target_col])

    colunas_texto = ['descricao', 'observacao', 'comentarios', 'sintomas']
    for col in colunas_texto:
        if col in df.columns:
            df = df.drop(columns=col)

    cols_objeto = df.select_dtypes(include=['object']).columns.tolist()
    if target_col in cols_objeto:
        cols_objeto.remove(target_col)

    df = pd.get_dummies(df, columns=cols_objeto, drop_first=True)

    X = df.drop(columns=[target_col])
    y = df[target_col]

    return X, y
