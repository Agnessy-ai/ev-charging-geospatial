import pandas as pd
import geopandas as gpd
import folium

# Load data
df = pd.read_csv("data/ev_stations.csv")

# Drop rows with missing or non-numeric latitude/longitude
df = df.dropna(subset=["latitude", "longitude"])
df = df[pd.to_numeric(df["latitude"], errors='coerce').notnull()]
df = df[pd.to_numeric(df["longitude"], errors='coerce').notnull()]

# Convert to float (just in case they're stored as strings)
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
    crs="EPSG:4326"
)

# Create a base map centered at the average location
m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=14)

# Add markers for each EV station
for _, row in gdf.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['type']} Charger",
        icon=folium.Icon(color='green' if row['type'] == 'Fast' else 'blue')
    ).add_to(m)

# Save the map
m.save("maps/ev_station_map.html")
print("✅ Map saved to: maps/ev_station_map.html")
