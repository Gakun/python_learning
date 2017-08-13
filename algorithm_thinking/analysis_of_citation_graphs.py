"""
Python codes for Algorithon Thinking - Week 2- Analysis of Citation Graphs
"""

import urllib2
import matplotlib.pyplot as plt
import random


def make_complete_graph(num_nodes):
    """
    Takes the number of nodes and returns a dictionary
    corresponding to a complete directed graph with the specified number of nodes.
    """
    graph_dict = dict()
    for node in xrange(num_nodes):
        graph_dict[node] = set([head for head in xrange(num_nodes) if head != node])
    return graph_dict


def compute_in_degrees(diagraph):
    """
    Takes a directed graph and compute the in-degrees for the nodes in the graph
    """
    indeg = {node: 0 for node in diagraph}
    for node in diagraph:
        for head in diagraph[node]:
            indeg[head] += 1
    return indeg


def in_degree_distribution(diagraph):
    """
    Takes a directed graph and computes the unnormalized distribution of the in-degrees
    of the graph
    """
    indeg = compute_in_degrees(diagraph)
    indeg_dis = dict()
    for node in indeg:
        indeg_dis[indeg[node]] = indeg_dis.get(indeg[node], 0) + 1
    print indeg_dis
    return indeg_dis


def graph_loader(graph_url):
    """
    Loads graph from a given URL and represents it as a dictionary
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_dict = dict()
    count = 0
    for line in graph_file:
        count += 1
        line = line.split()
        graph_dict[int(line[0])] = set([int(head) for head in line[1:]])
    print "Loaded %d nodes in toatal" % count
    return graph_dict


def plot_in_degree_distrinbution(graph_dict):
    """
    Takes a graph (presented as dictionary) and plot it's in-degrees distribution
    """
    indeg_dis = in_degree_distribution(graph_dict)
    # Normalize the in-degree distribution
    indeg_dis_normalized = {node: indeg_dis[node] * 1.0 / len(graph_dict) for node in indeg_dis}
    # Make sure the sum of normalized in-degree distribution is 1.0
    assert abs(sum([indeg_dis_normalized[indeg] for indeg in indeg_dis_normalized]) - 1.0) < 0.000001,\
        'The sum of normalized indgrees is not 1.0'
    # x axis, in-degree 0 not included
    degrees_list = indeg_dis_normalized.keys()[1:]
    degrees_list.sort()
    # print degrees_list
    # y axis, p-value
    p_list = [indeg_dis_normalized[degree] for degree in degrees_list]
    # Draw log-log plot
    plt.title('Citation Network: in-degree distribution')
    plt.xlabel('In-degree (log2)')
    plt.ylabel('p (log2)')
    plt.loglog(degrees_list, p_list, basex=2, basey=2)


def make_ER_graph(nodes_num, p_value):
    """
    Use ER method to create a random directed graph based on the given number of nodes
    and the possibility of each edge, return the dictionary
    """
    graph_dict = dict()
    for node_i in xrange(nodes_num):
        graph_dict[node_i] = set([])
        for node_j in xrange(nodes_num):
            if node_i != node_j and random.random() < p_value:
                graph_dict[node_i].add(node_j)
    return graph_dict


# Question 1
# CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
# graph = graph_loader(CITATION_URL)
# plot_in_degree_distrinbution(graph)
# plt.show()

# Question 2
# ER_graph_1 = make_ER_graph(100, 0.1)
# ER_graph_2 = make_ER_graph(100, 0.2)
# ER_graph_3 = make_ER_graph(100, 0.3)
# plot_in_degree_distrinbution(ER_graph_1)
# plot_in_degree_distrinbution(ER_graph_2)
# plot_in_degree_distrinbution(ER_graph_3)
# plt.show()

# Question 3
# CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
# citation_graph = graph_loader(CITATION_URL)
# n = len(citation_graph)
# m = sum([len(citation_graph[node]) for node in citation_graph]) / n
# print n, m

# Question 4
