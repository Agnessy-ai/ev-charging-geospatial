from sklearn.cluster import DBSCAN
import numpy as np

def spatial_clustering(df):
    coords = df[['latitude', 'longitude']].values
    kms_per_radian = 6371.0088
    epsilon = 0.5 / kms_per_radian  # 0.5 km
    db = DBSCAN(eps=epsilon, min_samples=2, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    df['cluster'] = db.labels_
    return df
