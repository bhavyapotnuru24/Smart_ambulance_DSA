def min_edit_distance(str1, str2):
    """
    DSA Concept G: EDIT DISTANCE / DYNAMIC PROGRAMMING
    Calculates the Levenshtein distance between two strings using 2D DP matrix.

    Time Complexity: O(M * N)
    Space Complexity: O(M * N)

    Returns:
    - Minimum edit operations required to transform str1 into str2.
    """
    str1 = str1.lower().strip()
    str2 = str2.lower().strip()

    m, n = len(str1), len(str2)

    # dp[i][j] stores minimum operations to convert str1[0..i-1] to str2[0..j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming to empty string
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Characters match, no edit needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Deletion
                    dp[i][j - 1],      # Insertion
                    dp[i - 1][j - 1]   # Substitution
                )

    return dp[m][n]


def fuzzy_search_patient(patient_list, search_name, max_distance=3):
    """
    Fuzzy search over patient records using Edit Distance.
    Returns patient with minimum edit distance within threshold.
    """
    best_patient = None
    best_distance = float('inf')

    for patient in patient_list:
        dist = min_edit_distance(search_name, patient.name)
        if dist < best_distance and dist <= max_distance:
            best_distance = dist
            best_patient = patient

    return best_patient, best_distance
