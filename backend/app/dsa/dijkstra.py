import heapq

def dijkstra_shortest_path(graph, start_node, target_node):
    """
    DSA Concept B: DIJKSTRA'S ALGORITHM
    Calculates the shortest weighted path from start_node to target_node.

    Parameters:
    - graph: Graph object containing adjacency list and coordinates.
    - start_node: e.g., 'USER_LOCATION'
    - target_node: e.g., 'HOSPITAL_1'

    Returns:
    - distance: Total distance in kilometers
    - path: List of node names along shortest route
    """
    # Priority Queue stores tuples of (current_distance, node_name, path_history)
    pq = []
    heapq.heappush(pq, (0.0, start_node, [start_node]))

    # Track minimum distance discovered to each node
    distances = {node: float('inf') for node in graph.adj}
    distances[start_node] = 0.0

    visited = set()

    while pq:
        current_dist, current_node, path = heapq.heappop(pq)

        if current_node == target_node:
            return round(current_dist, 2), path

        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, weight in graph.adj.get(current_node, []):
            if neighbor in visited:
                continue

            new_dist = current_dist + weight

            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))

    # Path not found fallback
    return float('inf'), []


def generate_candidate_routes(graph, start_node, hospital_nodes_map):
    """
    Computes shortest path using Dijkstra for eligible hospitals and formats candidate routes for UI display.
    """
    routes = []
    route_id = 1

    for hosp_node, hosp_obj in hospital_nodes_map.items():
        dist_km, path_nodes = dijkstra_shortest_path(graph, start_node, hosp_node)

        if dist_km == float('inf'):
            continue

        # Estimate travel time: Average city traffic speed ~30 km/h -> ~2 min per km
        eta_minutes = max(3, int(round(dist_km * 2.2)))

        # Build coordinate path for map polyline visualization
        coord_path = []
        for n in path_nodes:
            if n in graph.coordinates:
                coord_path.append(list(graph.coordinates[n]))

        routes.append({
            "route_id": route_id,
            "hospital": hosp_obj,
            "distance_km": dist_km,
            "eta_minutes": eta_minutes,
            "path_nodes": path_nodes,
            "coord_path": coord_path,
        })
        route_id += 1

    # Sort routes by distance/ETA
    routes.sort(key=lambda r: r["distance_km"])
    return routes
