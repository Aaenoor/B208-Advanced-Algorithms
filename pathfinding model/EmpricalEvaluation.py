import networkx as nx
import osmnx as ox
import geopandas as gpd
import time
import tracemalloc

def dijkstra(graph, start, end):
    return nx.shortest_path(graph, start, end, weight='length')

def a_star(graph, start, end):
    def heuristic(u, v):
        y1, x1 = graph.nodes[u]['y'], graph.nodes[u]['x']
        y2, x2 = graph.nodes[v]['y'], graph.nodes[v]['x']
        return ox.distance.euclidean(y1, x1, y2, x2)
    
    return nx.astar_path(graph, start, end, heuristic=heuristic, weight='length')

def get_nearest_hospital(graph, hospitals, point):
    nearest_node = ox.distance.nearest_nodes(graph, point[1], point[0])
    hospital_nodes = [ox.distance.nearest_nodes(graph, hospital.geometry.x, hospital.geometry.y) for hospital in hospitals.itertuples()]
    nearest_hospital_node = min(hospital_nodes, key=lambda x: nx.shortest_path_length(graph, nearest_node, x, weight='length'))
    hospital_name = hospitals[hospitals.apply(lambda row: ox.distance.nearest_nodes(graph, row.geometry.x, row.geometry.y) == nearest_hospital_node, axis=1)].iloc[0]['name']
    return nearest_hospital_node, hospital_name

def get_shortest_path(graph, hospitals, start_point):
    start_node = ox.distance.nearest_nodes(graph, start_point[1], start_point[0])
    nearest_hospital_node, hospital_name = get_nearest_hospital(graph, hospitals, start_point)
    path_dijkstra = dijkstra(graph, start_node, nearest_hospital_node)
    path_a_star = a_star(graph, start_node, nearest_hospital_node)
    return path_dijkstra, path_a_star, hospital_name

def get_path_edges(graph, path):
    edges = []
    for i in range(len(path) - 1):
        edge_data = graph.get_edge_data(path[i], path[i + 1])
        if edge_data:
            edge = edge_data[0]
            if isinstance(edge.get('name', 'Unnamed Road'), list):
                edges.extend(edge.get('name', 'Unnamed Road'))
            else:
                edges.append(edge.get('name', 'Unnamed Road'))
    return edges

def simplify_path(edges):
    simplified_edges = []
    for i, edge in enumerate(edges):
        if i == 0 or edge != edges[i - 1]:
            simplified_edges.append(edge)
    return simplified_edges

def format_path(road_sequence):
    if not road_sequence:
        return "No roads available."
    
    formatted_instructions = []
    for i, road in enumerate(road_sequence):
        if i == 0:
            formatted_instructions.append(f"Start by taking {road} road")
        elif i == len(road_sequence) - 1:
            formatted_instructions.append(f"and finally, take {road} road to reach your destination.")
        else:
            formatted_instructions.append(f"then continue on {road} road")
    return " ".join(formatted_instructions)

def measure_performance(start_point, G, hospitals):
    start_time = time.time()
    tracemalloc.start()
    
    path_dijkstra, path_a_star, hospital_name = get_shortest_path(G, hospitals, start_point)
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    
    runtime = end_time - start_time
    memory_usage = peak / 10**6  # Convert to MB
    
    return path_dijkstra, path_a_star, hospital_name, runtime, memory_usage

def main():
    # Load the graph and hospitals data
    G = ox.load_graphml('Heidelberg, Germany_mapped.graphml')
    hospitals = gpd.read_file('Heidelberg, Germany_hospitals.geojson')
    
    scenarios = {
        "Neuenheim (North Heidelberg)": (49.4217, 8.6815),
        "Heidelberg Zoo (West Heidelberg)": (49.4183, 8.6691),
        "Heidelberg-Süd (South Heidelberg)": (49.4039, 8.6732),
        "Handschuhsheim (North-East Heidelberg)": (49.4265, 8.6893),
        "Boxberg (South-West Heidelberg)": (49.3750, 8.6936)
    }
    
    results = []
    
    for scenario, coordinates in scenarios.items():
        print(f"\nScenario: {scenario}")
        
        path_dijkstra, path_a_star, hospital_name, runtime, memory_usage = measure_performance(coordinates, G, hospitals)
        
        edges_dijkstra = get_path_edges(G, path_dijkstra)
        edges_a_star = get_path_edges(G, path_a_star)
        
        simplified_edges_dijkstra = simplify_path(edges_dijkstra)
        simplified_edges_a_star = simplify_path(edges_a_star)
        
        formatted_dijkstra = format_path(simplified_edges_dijkstra)
        formatted_a_star = format_path(simplified_edges_a_star)
        
        result = {
            "scenario": scenario,
            "hospital_name": hospital_name,
            "dijkstra_path": formatted_dijkstra,
            "a_star_path": formatted_a_star,
            "runtime": runtime,
            "memory_usage": memory_usage
        }
        
        results.append(result)
        
        print(f"Nearest hospital: {hospital_name}")
        print(f"Runtime: {runtime:.2f} seconds")
        print(f"Memory usage: {memory_usage:.2f} MB")
        
        print("\nThe shortest path to the nearest hospital using Dijkstra's algorithm is:")
        print(formatted_dijkstra)
        
        print("\nThe shortest path to the nearest hospital using A* algorithm is:")
        print(formatted_a_star)
        
    return results

if __name__ == "__main__":
    results = main()
