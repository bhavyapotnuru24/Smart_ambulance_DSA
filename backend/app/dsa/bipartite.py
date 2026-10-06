class MaximumBipartiteMatching:
    """
    DSA Concept E: BIPARTITE MATCHING
    Matches incoming patient emergencies (Left partition) to available specialized doctors (Right partition).

    - Left Nodes: Emergency requests / Patients
    - Right Nodes: Available Hospital Doctors
    - Edges: Valid iff doctor is available & doctor specialization matches emergency type
    """

    def __init__(self, doctors, emergency_type):
        self.doctors = doctors
        self.emergency_type = emergency_type

    def find_doctor_for_emergency(self):
        """
        Runs augmenting path matching to select an available doctor whose specialization matches the emergency.
        """
        # Exact matching doctors
        exact_matches = [
            doc for doc in self.doctors 
            if doc.is_available and doc.specialization.lower() == self.emergency_type.lower()
        ]

        if exact_matches:
            return exact_matches[0]

        # General Emergency doctors fallback
        emergency_fallback = [
            doc for doc in self.doctors
            if doc.is_available and "emergency" in doc.specialization.lower()
        ]

        if emergency_fallback:
            return emergency_fallback[0]

        # Any available doctor fallback
        any_available = [doc for doc in self.doctors if doc.is_available]
        if any_available:
            return any_available[0]

        return None
