from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def cluster_players(df, n_clusters=3):
    features = df[["duration_sec", "applesEaten", "movements_count"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X_scaled)
    return df, kmeans
