import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt

def map_graph(city):
    G = ox.graph_from_place(city, network_type='drive')
    
    hospitals = gpd.read_file('Heidelberg, Germany_hospitals.geojson')
    
    for hospital in hospitals.itertuples():
        if hospital.geometry.geom_type == 'Point':
            hospital_node = ox.distance.nearest_nodes(G, hospital.geometry.x, hospital.geometry.y)
            G.nodes[hospital_node]['hospital'] = hospital.name
    
    return G

city = 'Heidelberg, Germany'
G = map_graph(city)

fig, ax = ox.plot_graph(G, show=False, close=False)

ox.save_graphml(G, filepath='Heidelberg, Germany_mapped.graphml')

plt.show()
