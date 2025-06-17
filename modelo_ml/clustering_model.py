from sklearn.cluster import KMeans

def train_kmeans(df, n_clusters=3):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = model.fit_predict(df)
    df_clustered = df.copy()
    df_clustered['cluster'] = clusters
    return model, df_clustered
