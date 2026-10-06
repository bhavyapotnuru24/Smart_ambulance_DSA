import heapq

class EmergencyPriorityQueue:
    """
    DSA Concept C: PRIORITY QUEUE
    Prioritizes emergency requests using Python's heapq (Min-Heap).
    Priority mapping:
    - Chest Pain: Priority 1 (Highest)
    - Breathing Problem: Priority 1 (Highest)
    - Accident / Injury: Priority 2 (High)
    - Other: Priority 3 (Normal)
    """

    PRIORITY_MAP = {
        "Chest Pain": (1, "High"),
        "Breathing Problem": (1, "High"),
        "Accident / Injury": (2, "High"),
        "Other": (3, "Normal")
    }

    def __init__(self):
        self._heap = []
        self._counter = 0  # Sequence number to break priority ties in FIFO order

    def push(self, emergency_data):
        """Pushes an emergency request into priority queue."""
        emergency_type = emergency_data.get("emergency_type", "Other")
        priority_rank, priority_label = self.PRIORITY_MAP.get(emergency_type, (3, "Normal"))

        self._counter += 1
        # Store tuple: (priority_rank, sequence_counter, emergency_data, priority_label)
        heapq.heappush(self._heap, (priority_rank, self._counter, emergency_data, priority_label))

    def pop(self):
        """Pops highest priority emergency request."""
        if not self._heap:
            return None
        priority_rank, _, emergency_data, priority_label = heapq.heappop(self._heap)
        emergency_data["priority"] = priority_label
        return emergency_data

    def peek(self):
        """Peeks at highest priority request without removing it."""
        if not self._heap:
            return None
        return self._heap[0][2]

    def get_priority_label(self, emergency_type):
        """Helper to return priority level string ('High' or 'Normal')."""
        _, label = self.PRIORITY_MAP.get(emergency_type, (3, "Normal"))
        return label
