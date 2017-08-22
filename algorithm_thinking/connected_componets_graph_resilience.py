"""
Computing the set of connected components (CCs) of an undirected graph and determining the size of its largest connected componets
by implementing Breadth-first Search.
"""

from collections import deque


def bfs_visited(ugraph, start_node):
    """
    Takes a undirected graph and start node,
    return its connected nodes by using BFS
    """
    visited = set([start_node])
    que = deque()
    que.append(start_node)
    while len(que) != 0:
        node = que.popleft()
        for neighbor in ugraph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                que.append(neighbor)
    return visited


def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets of connected nodes
    """
    connected_nodes = list()
    remained_nodes = set(ugraph.keys())
    while len(remained_nodes) != 0:
        source_node = remained_nodes.pop()
        visited = bfs_visited(ugraph, source_node)
        connected_nodes.append(visited)
        remained_nodes.difference_update(visited)
    return connected_nodes


def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size (integer) of the largest
    connected componet in ugraph
    """
    connected_comp = cc_visited(ugraph)
    max_size = 0
    for comp in connected_comp:
        if len(comp) > max_size:
            max_size = len(comp)
    return max_size


def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order, compute the resilience
    after removing the node and its edges in attack_order.
    """
    resilience = list()
    resilience.append(largest_cc_size(ugraph))
    for attack in attack_order:
        # Remove the edge from the nodes of other side
        for other_node in ugraph[attack]:
            ugraph[other_node].discard(attack)
        # Remove all the edge of the node being attack
        ugraph.pop(attack)
        resilience.append(largest_cc_size(ugraph))
    return resilience


def test_bfs_visited():
    """
    Test 1 - bfs_visited
    """
    case = {0: set([])}
    print bfs_visited(case, 0)

    case = {0: set([2]), 1: set([2, 3]), 2: set([0, 1, 3]), 3: set([1, 2]), 4: set([5]), 5: set([4])}
    print bfs_visited(case, 0)
    print bfs_visited(case, 4)


def test_cc_visited():
    """
    Test 2- cc_visited
    """
    case = {0: set([])}
    print cc_visited(case)

    case = {0: set([2]), 1: set([2, 3]), 2: set([0, 1, 3]), 3: set([1, 2]), 4: set([5]), 5: set([4])}
    print cc_visited(case)


def test_largest_cc_size():
    """
    Test 3 - largest_cc_size
    """
    case = {0: set([])}
    print largest_cc_size(case)

    case = {0: set([2]), 1: set([2, 3]), 2: set([0, 1, 3]), 3: set([1, 2]), 4: set([5]), 5: set([4])}
    print largest_cc_size(case)


def test_compute_resilience():
    """
    Test 4 - compute_resilience
    """
    ugraph = {0: set([2]), 1: set([2, 3]), 2: set([0, 1, 3]), 3: set([1, 2]), 4: set([5]), 5: set([4])}
    attack_order = [2, 0, 4, 1]
    print compute_resilience(ugraph, attack_order)
#test_bfs_visited()
#test_cc_visited()
#test_largest_cc_size()
#test_compute_resilience()
