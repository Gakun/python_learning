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


def plot_in_degree_distrinbution(graph_dict_list, title, xlabel, ylabel, legend_list=['']):
    """
    Takes list of multiple graphs (presented as dictionary) and plot their in-degrees distribution
    """
    for graph_num in range(len(graph_dict_list)):
        graph_dict = graph_dict_list[graph_num]
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
        plt.loglog(degrees_list, p_list, basex=2, basey=2, label=legend_list[graph_num])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()


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


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm

    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def make_DPA_graph(final_nodes, edge_add):
    """
    Use DPA method to create a random directed graph based on the given final_nodes and edge_add in
    each iteration

    DPA - Directed graph with Preferential Attachment
    """
    # Create a complete graph on edge_add nodes
    graph_dict = make_complete_graph(edge_add)
    dpa_trial = DPATrial(edge_add)
    for node in range(edge_add, final_nodes):
        new_neighbors = dpa_trial.run_trial(edge_add)
        graph_dict[node] = new_neighbors
        # print graph_dict
    return graph_dict


#Question 1
# CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
# graph = graph_loader(CITATION_URL)
# plot_in_degree_distrinbution([graph], 'In-degree Distribution: citation graph', 'in-degrees (log2)', 'p (log2)')

# Question 2
# ER_graph_1 = make_ER_graph(100, 0.1)
# ER_graph_2 = make_ER_graph(100, 0.2)
# ER_graph_3 = make_ER_graph(100, 0.3)
# plot_in_degree_distrinbution([ER_graph_1, ER_graph_2, ER_graph_3], 'In-degree Distribution: ER Graph',
#     'in-degrees (log2)', 'p (log2)', legend_list=['n=100, p=0.1', 'n=100, p=0.2', 'n=100, p=0.3'])

# Question 3
# CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
# citation_graph = graph_loader(CITATION_URL)
# n = len(citation_graph)
# m = sum([len(citation_graph[node]) for node in citation_graph]) / n
# print n, m

# Question 4 - final_nodes = 27770, edge_add = 12
CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
citation_graph = graph_loader(CITATION_URL)
dpa_graph = make_DPA_graph(27770, 12)
plot_in_degree_distrinbution([citation_graph, dpa_graph], 'in-degree Distribution',
    'in-degrees (log2)', 'p (log2)', legend_list=['Citation Graph', 'DPA Graph'])
