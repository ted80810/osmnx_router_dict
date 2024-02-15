# route_processor.py

import osmnx as ox
import numpy as np
import networkx as nx
import warnings
warnings.filterwarnings("ignore")

def process_segment(segment):
    start, end = segment
    start_coord = start
    end_coord = end

    try:
        # Create graph from the street network
        G = ox.graph_from_point((start_coord[1], start_coord[0]), network_type='drive')

        # Check if start and end nodes are in the graph
        start_node = ox.distance.nearest_nodes(G, start_coord[1], start_coord[0], return_dist=False)
        end_node = ox.distance.nearest_nodes(G, end_coord[1], end_coord[0], return_dist=False)
        if not start_node or not end_node:
            raise nx.NodeNotFound("Either source or target node is not in the graph")

        # Calculate the shortest path
        route = ox.shortest_path(G, start_node, end_node, weight='length')

        # Extracting route information
        route_length = sum(ox.utils_graph.get_route_edge_attributes(G, route, 'length'))
        route_speeds = ox.utils_graph.get_route_edge_attributes(G, route, 'maxspeed')
        route_grade = ox.utils_graph.get_route_edge_attributes(G, route, 'grade_abs')

        # Compute time
        speed = np.mean(route_speeds) if route_speeds else 10.0  # Assuming average speed of 10 m/s if speed data is missing
        time = route_length / speed

        return {
            "distance": route_length,
            "speed": speed,
            "time": time,
            "grade": np.mean(route_grade) if route_grade else None,
            "seg_end": end_coord,
            "direction": "",  # You need to implement logic to determine direction
            "intersect": ""   # You need to implement logic to determine intersection info
        }
    except nx.NodeNotFound as e:
        # Handle NodeNotFound exception
        print(f"Node not found: {e}")
        return None  # Return None for the segment that caused the error
    except nx.NetworkXNoPath:
        # Handle NetworkXNoPath exception (no path found)
        print(f"No path found for segment: {segment}")
        return None  # Return None for the segment that caused the error
