"""
Codes for Algorithm Thinking Application 3
"""
import alg_project3_solution as solution
import alg_cluster
import random
import time
import matplotlib.pyplot as plt
import urllib2
import copy

def gen_random_clusters(num_clusters):
    """
    Creates a list of clusters where each cluster corresponds to one randomly generated point in the square
    wiht corners (+-1, +- 1)
    """
    cluster_list = list()
    for dummy_idx in xrange(num_clusters):
        x_pos = random.random() * 2 - 1
        y_pos = random.random() * 2 - 1
        cluster = alg_cluster.Cluster(set(), x_pos, y_pos, 0, 0)
        cluster_list.append(cluster)
    return cluster_list


def compare_line_plot(x_list, y_list, x_label, y_label, legend_list=[''], title=''):
    """
    Plot multiple line plots
    """
    for idx in xrange(len(y_list)):
        plt.plot(x_list[idx], y_list[idx], label=legend_list[idx])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()


def compute_distortion(cluster_list, data_table):
    """
    Takes a list of clusters and uses cluster_error to compute its distortion.
    """
    result = sum([cluster.cluster_error(data_table) for cluster in cluster_list])
    return result


def q1_solution():
    """
    Code for Question 1
    """
    slow_result = list()
    fast_result = list()
    for size in xrange(2, 201):
        cluster_list = gen_random_clusters(size)
        start_time = time.time()
        solution.slow_closest_pair(cluster_list)
        slow_result.append(time.time() - start_time)

        start_time = time.time()
        solution.fast_closest_pair(cluster_list)
        fast_result.append(time.time() - start_time)
    #Create Plot
    compare_line_plot([range(2, 201), range(2, 201)], [slow_result, fast_result], 'Number of Initial Clusters'
        , 'Running Time (seconds)', legend_list=['slow_closest_pair', 'fast_closest_pair'],
        title='Running Time of Two Closest Pair methods')

#q1_solution()


DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])]
            for tokens in data_tokens]


def q7_solution():
    """
    Code for Question 7
    Hierarchical: 1.752*10^11
    K-means: 2.713*10^11
    """
    data_table = load_data_table(DATA_111_URL)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    #cluster_list = sequential_clustering(singleton_list, 15)
    #print "Displaying", len(cluster_list), "sequential clusters"

    cluster_list = solution.hierarchical_clustering(singleton_list, 9)
    print "Displaying", len(cluster_list), "hierarchical clusters"
    print compute_distortion(cluster_list, data_table)

    # cluster_list = solution.kmeans_clustering(singleton_list, 9, 5)
    # print "Displaying", len(cluster_list), "k-means clusters"
    # print compute_distortion(cluster_list, data_table)

#q7_solution()


def q10_solution():
    """
    Question 10
    """
    cluster_range = range(6, 21)
    hier_dist = list()
    kmeans_dist = list()
    data_table = load_data_table(DATA_896_URL)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    hier_singleton = copy.deepcopy(singleton_list)
    # Compute distortion of hierarchical cluster
    hier_cluster = solution.hierarchical_clustering(hier_singleton, 20)
    hier_dist.append(compute_distortion(hier_cluster, data_table))
    for num in xrange(19, 5, -1):
        hier_cluster = solution.hierarchical_clustering(hier_cluster, num)
        hier_dist.append(compute_distortion(hier_cluster, data_table))
    hier_dist.reverse()
    # Compute distortion of k-means cluster
    for num in cluster_range:
        kmeans_singleton = copy.deepcopy(singleton_list)
        kmeans_dist.append(compute_distortion(solution.kmeans_clustering(kmeans_singleton, num, 5), data_table))
    # Plot
    compare_line_plot([cluster_range, cluster_range], [hier_dist, kmeans_dist],
        'Number of Clusters', 'Distortion (10^12)', legend_list=['Hierarchical', 'K-means'],
        title='Distortion of Two Clustering Methods \n- 896 Data Set')

q10_solution()
