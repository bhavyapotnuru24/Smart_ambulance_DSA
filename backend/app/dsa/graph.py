import math

class Graph:
    """
    DSA Concept A: GRAPH REPRESENTATION
    Represents the Hyderabad road network.
    - Vertices: Road intersections and Hospital locations.
    - Edges: Connecting roads between locations.
    - Weights: Distance in kilometers (or estimated travel time).
    """

    def __init__ (self):
        # Adjacency list: node_name -> list of (neighbor_name, weight_km)
        self.adj = {}
        # Node coordinates: node_name -> (latitude, longitude)
        self.coordinates = {}

    def add_node(self, name, lat, lng):
        """Add a vertex/node with its geographical coordinates."""
        if name not in self.adj:
            self.adj[name] = []
        self.coordinates[name] = (lat, lng)

    def add_edge(self, u, v, weight, bidirectional=True):
        """Add a weighted edge between vertex u and vertex v."""
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []

        self.adj[u].append((v, weight))
        if bidirectional:
            self.adj[v].append((u, weight))

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate straight-line distance in km using Haversine formula."""
        R = 6371.0  # Radius of Earth in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    def build_hyderabad_network(self, hospitals):
        """
        Builds a realistic road network for Hyderabad with key intersections and connected hospitals.
        """
        # Key Intersections
        intersections = {
            "Jubilee Hills Checkpost": (17.4300, 78.4080),
            "Banjara Hills Circle": (17.4150, 78.4450),
            "Begumpet Junction": (17.4440, 78.4680),
            "Secunderabad Station": (17.4340, 78.5010),
            "Gachibowli Flyover": (17.4350, 78.3750),
            "Financial District": (17.4200, 78.3450),
            "Nampally Junction": (17.3900, 78.4700),
        }

        for name, (lat, lng) in intersections.items():
            self.add_node(name, lat, lng)

        # Connect Intersections (Road network with realistic distances in km)
        self.add_edge("Jubilee Hills Checkpost", "Banjara Hills Circle", 3.2)
        self.add_edge("Jubilee Hills Checkpost", "Gachibowli Flyover", 6.5)
        self.add_edge("Banjara Hills Circle", "Begumpet Junction", 4.8)
        self.add_edge("Banjara Hills Circle", "Nampally Junction", 4.0)
        self.add_edge("Begumpet Junction", "Secunderabad Station", 3.5)
        self.add_edge("Gachibowli Flyover", "Financial District", 3.8)
        self.add_edge("Nampally Junction", "Secunderabad Station", 6.2)

        # Add Hospital Nodes and connect each hospital to nearest road intersections
        for h in hospitals:
            h_node = f"HOSPITAL_{h.id}"
            self.add_node(h_node, h.latitude, h.longitude)

            # Find closest 2 intersections to connect hospital to graph
            closest = []
            for inter_name, (i_lat, i_lng) in intersections.items():
                dist = self.haversine_distance(h.latitude, h.longitude, i_lat, i_lng)
                closest.append((dist, inter_name))
            closest.sort()

            # Connect hospital to nearest 2 intersections
            for dist, inter_name in closest[:2]:
                self.add_edge(h_node, inter_name, max(0.5, dist))

    def connect_user_location(self, user_lat, user_lng):
        """Dynamically add USER node and connect to closest 3 road network intersections."""
        user_node = "USER_LOCATION"
        self.add_node(user_node, user_lat, user_lng)

        # Connect user to nearest road network nodes
        distances = []
        for node, (lat, lng) in self.coordinates.items():
            if node != user_node and not node.startswith("HOSPITAL_"):
                dist = self.haversine_distance(user_lat, user_lng, lat, lng)
                distances.append((dist, node))
        distances.sort()

        # Connect to 3 nearest intersections
        for dist, inter_name in distances[:3]:
            self.add_edge(user_node, inter_name, max(0.2, dist))

        return user_node
