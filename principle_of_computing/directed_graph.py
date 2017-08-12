"""
Functions used to presented a give directed graph as dictionary,
and compute the distribution of the in-degrees for nodes of it
"""

EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}
EX_GRAPH2 = {0: {1, 4, 5}, 1: {2, 6}, 2: {3, 7}, 3: {7}, 4: {1}, 5: {2}, 6: set([]), 7: {3}, 8: {1, 2}, 9: {0, 3, 4, 5, 6, 7}}


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


def test_make_complete_graph():
    """
    Test make_complete_graph
    """
    print make_complete_graph(1)
    print make_complete_graph(2)
    print make_complete_graph(4)


def test_compute_in_degrees():
    """
    Test compute_in_degrees
    """
    print compute_in_degrees(EX_GRAPH0)
    print compute_in_degrees(EX_GRAPH1)
    print compute_in_degrees(EX_GRAPH2)


def test_in_degree_distribution():
    """
    Test in_degree_distribution
    """
    print in_degree_distribution(EX_GRAPH0)
    print in_degree_distribution(EX_GRAPH1)
    print in_degree_distribution(EX_GRAPH2)


test_make_complete_graph()
test_compute_in_degrees()
test_in_degree_distribution()
