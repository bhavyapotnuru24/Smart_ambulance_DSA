def compute_lps_array(pattern):
    """
    Computes Longest Prefix Suffix (LPS) array for KMP algorithm.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i].lower() == pattern[length].lower():
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    """
    DSA Concept F: KMP STRING MATCHING ALGORITHM
    Searches for exact substring occurrence of 'pattern' in 'text'.
    Time Complexity: O(N + M) where N = len(text), M = len(pattern).

    Returns:
    - True if pattern is found in text, else False.
    """
    if not pattern or not text:
        return False

    text_lower = text.lower()
    pattern_lower = pattern.lower()

    n = len(text_lower)
    m = len(pattern_lower)

    if m > n:
        return False

    lps = compute_lps_array(pattern_lower)

    i = 0  # index for text_lower
    j = 0  # index for pattern_lower

    while i < n:
        if pattern_lower[j] == text_lower[i]:
            i += 1
            j += 1

        if j == m:
            return True  # Found exact pattern match!
        elif i < n and pattern_lower[j] != text_lower[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False


def search_patient_kmp(patient_list, search_name):
    """
    Searches list of patient records using KMP exact matching.
    """
    for patient in patient_list:
        if kmp_search(patient.name, search_name) or kmp_search(search_name, patient.name):
            return patient
    return None
