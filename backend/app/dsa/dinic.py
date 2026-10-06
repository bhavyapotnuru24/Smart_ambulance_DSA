from collections import deque

class Edge:
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0
        self.rev = None  # Reference to reverse residual edge


class DinicMaxFlow:
    """
    DSA Concept D: MAX FLOW / DINIC'S ALGORITHM
    Models hospital bed allocation capacity.
    - Source S connected to Hospitals with capacity = available_beds.
    - If available_beds == 0, edge capacity is 0, guaranteeing zero flow.
    - Hospitals connected to Sink T.
    """

    def __init__(self, num_vertices):
        self.n = num_vertices
        self.graph = [[] for _ in range(num_vertices)]
        self.level = []

    def add_edge(self, u, v, capacity):
        forward = Edge(u, v, capacity)
        backward = Edge(v, u, 0)
        forward.rev = backward
        backward.rev = forward
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def _bfs(self, s, t):
        """Builds Level Graph using BFS."""
        self.level = [-1] * self.n
        self.level[s] = 0
        queue = deque([s])

        while queue:
            u = queue.popleft()
            for edge in self.graph[u]:
                if edge.capacity - edge.flow > 0 and self.level[edge.v] < 0:
                    self.level[edge.v] = self.level[u] + 1
                    queue.append(edge.v)

        return self.level[t] >= 0

    def _send_flow(self, u, flow, t, ptr):
        """Sends blocking flow in Level Graph using DFS."""
        if u == t:
            return flow

        while ptr[u] < len(self.graph[u]):
            edge = self.graph[u][ptr[u]]

            if self.level[edge.v] == self.level[u] + 1 and edge.capacity - edge.flow > 0:
                current_flow = min(flow, edge.capacity - edge.flow)
                temp_flow = self._send_flow(edge.v, current_flow, t, ptr)

                if temp_flow > 0:
                    edge.flow += temp_flow
                    edge.rev.flow -= temp_flow
                    return temp_flow

            ptr[u] += 1

        return 0

    def max_flow(self, s, t):
        """Calculates Maximum Flow from Source s to Sink t."""
        total_flow = 0

        while self._bfs(s, t):
            ptr = [0] * self.n
            while True:
                flow = self._send_flow(s, float('inf'), t, ptr)
                if flow == 0:
                    break
                total_flow += flow

        return total_flow


def verify_hospital_bed_capacity_flow(hospitals):
    """
    Constructs a flow network using Dinic's algorithm to compute total available bed capacity across hospitals.
    If a hospital has 0 available beds, its capacity in the flow network is 0.
    """
    # Nodes: 0 = Source, 1..N = Hospitals, N+1 = Sink
    num_hospitals = len(hospitals)
    source = 0
    sink = num_hospitals + 1

    dinic = DinicMaxFlow(num_vertices=sink + 1)

    hospital_capacities = {}

    for idx, h in enumerate(hospitals, start=1):
        cap = max(0, h.available_beds)
        dinic.add_edge(source, idx, cap)
        dinic.add_edge(idx, sink, cap)
        hospital_capacities[h.id] = cap

    max_bed_flow = dinic.max_flow(source, sink)

    return {
        "max_flow_bed_capacity": max_bed_flow,
        "hospital_capacities": hospital_capacities
    }
