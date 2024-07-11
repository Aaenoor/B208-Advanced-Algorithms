import osmnx as ox
import geopandas as gpd

def collect_data(city):
    tags = {'amenity': 'hospital'}
    
    hospitals = ox.features_from_place(city, tags)  # Updated to use features_from_place
    G = ox.graph_from_place(city, network_type='drive')
    
    hospitals = hospitals[hospitals.geometry.type == 'Point']
    
    for col in hospitals.columns:
        if hospitals[col].apply(lambda x: isinstance(x, list)).any():
            hospitals = hospitals.drop(columns=[col])
    
    hospitals.to_file(f"{city}_hospitals.geojson", driver='GeoJSON')
    
    ox.save_graphml(G, filepath=f"{city}.graphml")
    
    return G, hospitals

city = 'Heidelberg, Germany'

G, hospitals = collect_data(city)
