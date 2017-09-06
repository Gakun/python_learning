"""
Solution for the ALgorithm Thinking Project 4
"""


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores,
    returns a dictionary of dictionaries represents the score matrix
    """
    alphabet = list(alphabet)
    alphabet.append('-')
    score_matrix = dict()
    for char in alphabet:
        score_matrix[char] = dict()
    for char_x in score_matrix:
        for char_y in alphabet:
            if char_x == '-' or char_y == '-':
                score_matrix[char_x][char_y] = dash_score
            elif char_x == char_y:
                score_matrix[char_x][char_y] = diag_score
            else:
                score_matrix[char_x][char_y] = off_diag_score
    return score_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y and scoring_matrix,
    return the alignment matrix for two sequences according to global_flag
    """
    height = len(seq_x)
    width = len(seq_y)
    # Initial matrix
    align_matrix = [[0 for dummy_x in range(width + 1)] for dummy_y in range(height + 1)]
    # If global alignment
    if global_flag:
        # Initial S[i, 0]
        for idx_i in range(1, height + 1):
            align_matrix[idx_i][0] = align_matrix[idx_i - 1][0] + scoring_matrix[seq_x[idx_i - 1]]['-']
        # Initial S[0, j]
        for idx_j in range(1, width + 1):
            align_matrix[0][idx_j] = align_matrix[0][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]]
        # Compute rest score
        for idx_i in range(1, height + 1):
            for idx_j in range(1, width + 1):
                score1 = align_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]
                score2 = align_matrix[idx_i][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]]
                score3 = align_matrix[idx_i - 1][idx_j] + scoring_matrix[seq_x[idx_i - 1]]['-']
                align_matrix[idx_i][idx_j] = max(score1, score2, score3)
    # If local alignment
    else:
        for idx_i in range(1, height + 1):
            align_matrix[idx_i][0] = max(align_matrix[idx_i - 1][0] + scoring_matrix[seq_x[idx_i - 1]]['-'], 0)
        # Initial S[0, j]
        for idx_j in range(1, width + 1):
            align_matrix[0][idx_j] = max(align_matrix[0][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]], 0)
        # Compute rest score
        for idx_i in range(1, height + 1):
            for idx_j in range(1, width + 1):
                score1 = align_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]
                score2 = align_matrix[idx_i][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]]
                score3 = align_matrix[idx_i - 1][idx_j] + scoring_matrix[seq_x[idx_i - 1]]['-']
                align_matrix[idx_i][idx_j] = max(score1, score2, score3, 0)

    return align_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y and computes a global alignment,
    returns a tuple: (max_score, align_x, align_y)
    """
    idx_i = len(seq_x)
    idx_j = len(seq_y)
    align_x = ''
    align_y = ''

    while idx_i != 0 and idx_j != 0:
        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]:
            align_x = seq_x[idx_i - 1] + align_x
            align_y = seq_y[idx_j - 1] + align_y
            idx_i -= 1
            idx_j -= 1
        elif alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]]:
            align_x = '-' + align_x
            align_y = seq_y[idx_j - 1] + align_y
            idx_j -= 1
        else:
            align_x = seq_x[idx_i - 1] + align_x
            align_y = '-' + align_y
            idx_i -= 1

    # Compute the rest of sequence
    while idx_i != 0:
        align_x = seq_x[idx_i - 1] + align_x
        align_y = '-' + align_y
        idx_i -= 1
    while idx_j != 0:
        align_x = '-' + align_x
        align_y = seq_y[idx_j - 1] + align_y
        idx_j -= 1
    return (alignment_matrix[len(seq_x)][len(seq_y)], align_x, align_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y and computes a local alignment,
    returns a tuple: (max_score, align_x, align_y)
    """
    start = max([(idx_i, idx_j) for idx_i in range(len(seq_x) + 1) for idx_j in range(len(seq_y) + 1)],
        key = lambda pair: alignment_matrix[pair[0]][pair[1]])
    idx_i = start[0]
    idx_j = start[1]
    max_score = alignment_matrix[idx_i][idx_j]
    align_x = ''
    align_y = ''

    while idx_i != 0 and idx_j != 0 and alignment_matrix[idx_i][idx_j] > 0:
        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]:
            align_x = seq_x[idx_i - 1] + align_x
            align_y = seq_y[idx_j - 1] + align_y
            idx_i -= 1
            idx_j -= 1
        elif alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]]:
            align_x = '-' + align_x
            align_y = seq_y[idx_j - 1] + align_y
            idx_j -= 1
        else:
            align_x = seq_x[idx_i - 1] + align_x
            align_y = '-' + align_y
            idx_i -= 1
    return (max_score, align_x, align_y)


def test_build_scoring_matrix():
    """
    Test - build_scoring_matrix
    """
    score_matrix = build_scoring_matrix(set(['A', 'T', 'C', 'G']), 10, 5, -5)
    for char in score_matrix:
        print char, score_matrix[char]


def test_compute_alignment_matrix():
    """
    Test - compute_alignment_matrix
    """
    score_matrix = build_scoring_matrix(set(['A', 'T', 'C', 'G']), 10, 4, -6)
    seq_x = 'AAAA'
    seq_y = 'AAAA'
    print compute_alignment_matrix(seq_x, seq_y, score_matrix, True)
    seq_x = 'AA'
    seq_y = 'TAAT'
    print compute_alignment_matrix(seq_x, seq_y, score_matrix, False)


def test_compute_global_alignment():
    """
    Test - compute_global_alignment
    """
    score_matrix = build_scoring_matrix(set(['A', 'T', 'C', 'G']), 10, 4, -6)
    seq_x = 'AA'
    seq_y = 'TAAT'
    align_matrix = compute_alignment_matrix(seq_x, seq_y, score_matrix, True)
    print align_matrix
    print compute_global_alignment(seq_x, seq_y, score_matrix, align_matrix)


def test_compute_local_alignment():
    """
    Test - compute_local_alignment
    """
    score_matrix = build_scoring_matrix(set(['A', 'T', 'C', 'G']), 10, 4, -6)
    seq_x = 'AA'
    seq_y = 'TAAT'
    align_matrix = compute_alignment_matrix(seq_x, seq_y, score_matrix, False)
    print align_matrix
    print compute_local_alignment(seq_x, seq_y, score_matrix, align_matrix)

# test_build_scoring_matrix()
# test_compute_alignment_matrix()
# test_compute_global_alignment()
# test_compute_local_alignment()
