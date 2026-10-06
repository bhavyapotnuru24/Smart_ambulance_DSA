import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.dsa.graph import Graph
from app.dsa.dijkstra import dijkstra_shortest_path
from app.dsa.priority_queue import EmergencyPriorityQueue
from app.dsa.kmp import kmp_search
from app.dsa.edit_distance import min_edit_distance
from app.dsa.dinic import DinicMaxFlow

def test_all():
    # 1. Test Priority Queue
    pq = EmergencyPriorityQueue()
    pq.push({"name": "Patient A", "emergency_type": "Other"})
    pq.push({"name": "Patient B", "emergency_type": "Chest Pain"})
    popped = pq.pop()
    print("Priority Queue Pop test:", popped["name"], popped["priority"])
    assert popped["name"] == "Patient B", "Chest Pain should have highest priority!"

    # 2. Test KMP
    assert kmp_search("Rahul Kumar", "Rahul") == True, "KMP exact match failed"
    assert kmp_search("Rahul Kumar", "Suresh") == False, "KMP false match failed"
    print("KMP Search test: PASSED")

    # 3. Test Edit Distance
    dist = min_edit_distance("Apolo", "Apollo")
    print(f"Edit Distance 'Apolo' vs 'Apollo': {dist}")
    assert dist == 1, "Edit distance should be 1"

    # 4. Test Graph & Dijkstra
    g = Graph()
    g.add_node("A", 17.4, 78.4)
    g.add_node("B", 17.5, 78.5)
    g.add_node("C", 17.6, 78.6)
    g.add_edge("A", "B", 5.0)
    g.add_edge("B", "C", 3.0)
    g.add_edge("A", "C", 10.0)
    d, p = dijkstra_shortest_path(g, "A", "C")
    print(f"Dijkstra Shortest Path A->C: dist={d}, path={p}")
    assert d == 8.0, "Dijkstra shortest path should be 8.0"

    # 5. Test Dinic Max Flow
    dinic = DinicMaxFlow(4)
    dinic.add_edge(0, 1, 10)  # Source -> Hosp1 (10 beds)
    dinic.add_edge(0, 2, 0)   # Source -> Hosp2 (0 beds)
    dinic.add_edge(1, 3, 10)  # Hosp1 -> Sink
    dinic.add_edge(2, 3, 0)   # Hosp2 -> Sink
    flow = dinic.max_flow(0, 3)
    print("Dinic Max Flow test:", flow)
    assert flow == 10, "Max flow should be 10"

    print("ALL DSA MODULES PASSED VERIFICATION!")

if __name__ == "__main__":
    test_all()
