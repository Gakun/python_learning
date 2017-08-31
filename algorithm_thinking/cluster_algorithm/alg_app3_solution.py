"""
Codes for Algorithm Thinking Application 3
"""
import alg_project3_solution as solution
import alg_cluster
import random
import time
import matplotlib.pyplot as plt
import urllib2
import alg_project

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


def q7_solution():
    """
    Code for Question 7
    """


