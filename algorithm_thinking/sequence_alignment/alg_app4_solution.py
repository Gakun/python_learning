"""
Provide code and solution for Application 4
"""

import math
import random
import urllib2


import matplotlib.pyplot as plt
import alg_project4_solution as student


# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


###############################################
# provided code


def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


def q1_solution():
    """
    Question 1 - solution
    (875, 
    'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ',
    'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ')
    """
    score_matrix = read_scoring_matrix(PAM50_URL)
    human_protein = read_protein(HUMAN_EYELESS_URL)
    fly_protein = read_protein(FRUITFLY_EYELESS_URL)
    align_matrix = student.compute_alignment_matrix(human_protein, fly_protein, score_matrix, False)
    return student.compute_local_alignment(human_protein, fly_protein, score_matrix, align_matrix)

#q1_solution()


def q2_solution():
    """
    Question 2 - solution
    local human vs consensus:  0.729323308271
    local fly vs consensus:  0.701492537313
    """
    local_align_result = q1_solution()
    human_local = local_align_result[1]
    fly_local = local_align_result[2]
    consensus = read_protein(CONSENSUS_PAX_URL)
    score_matrix = read_scoring_matrix(PAM50_URL)
    # Compute local human vs consensus
    # Remove '-'
    human_local = tuple([char for char in human_local if char != '-'])
    # Compute global align
    human_align_matrix = student.compute_alignment_matrix(human_local, consensus, score_matrix, True)
    human_consensus = student.compute_global_alignment(human_local, consensus, score_matrix, human_align_matrix)
    # Compute percentage of similarity
    count = 0
    for idx in range(len(human_consensus[1])):
        if human_consensus[1][idx] == human_consensus[2][idx]:
            count += 1
    print "local human vs consensus: ", float(count) / len(human_consensus[1])
    # Compute local fruitfly vs consensus
    # Remove '-'
    fly_local = tuple([char for char in fly_local if char != '-'])
    # Compute global align
    fly_align_matrix = student.compute_alignment_matrix(fly_local, consensus, score_matrix, True)
    fly_consensus = student.compute_global_alignment(fly_local, consensus, score_matrix, fly_align_matrix)
    # Compute percentage of similarity
    count = 0
    for idx in range(len(fly_consensus[1])):
        if fly_consensus[1][idx] == fly_consensus[2][idx]:
            count += 1
    print "local fly vs consensus: ", float(count) / len(fly_consensus[1])

# q2_solution()


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Takes as input two sequences, random shuffle seq_y, and compute the max score of aligning
    seq_x and rand_y. Do trials num_trials times.
    Return the score distribution as a dictionary
    """
    score_distribution = dict()
    while num_trials > 0:
        print "Rest of Trials: ", num_trials
        rand_y = list(seq_y)
        random.shuffle(rand_y)
        rand_y = tuple(rand_y)
        align_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, align_matrix)[0]
        score_distribution[score] = score_distribution.get(score, 0) + 1
        num_trials -= 1
    return score_distribution


def q4_solution():
    """
    Question 4 - solution
    """
    score_matrix = read_scoring_matrix(PAM50_URL)
    human_protein = read_protein(HUMAN_EYELESS_URL)
    fly_protein = read_protein(FRUITFLY_EYELESS_URL)
    score_distribution = generate_null_distribution(human_protein, fly_protein, score_matrix, 1000)
    # Normalize
    for score in score_distribution:
        score_distribution[score] = float(score_distribution[score]) / 1000

    # Plot
    x_series = score_distribution.keys()
    x_series.sort()
    y_series = [score_distribution[score] for score in x_series]
    plt.bar(x_series, y_series)
    plt.title('Scoring Distribution')
    plt.xlabel('Score')
    plt.ylabel('Fraction')
    plt.show()

q4_solution()





