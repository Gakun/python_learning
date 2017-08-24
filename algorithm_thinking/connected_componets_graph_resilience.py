"""
Computing the set of connected components (CCs) of an undirected graph and determining the size of its largest connected componets
by implementing Breadth-first Search.
"""

from collections import deque
import undirected_graph_sample as SAMPLE
import copy


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
    ugraph_copy = copy.deepcopy(ugraph)
    resilience = list()
    resilience.append(largest_cc_size(ugraph_copy))
    for attack in attack_order:
        # Remove the edge from the nodes of other side
        for other_node in ugraph_copy[attack]:
            ugraph_copy[other_node].discard(attack)
        # Remove all the edge of the node being attack
        ugraph_copy.pop(attack)
        resilience.append(largest_cc_size(ugraph_copy))
    return resilience


def compute_resilience_disjoint_set(ugraph, attack_order):
    """
    Asymptotically faster approaches of compute_resilience based on disjoint set algorithm
    """
    # Compute the final graph after all attacking
    attacked_graph = copy.deepcopy(ugraph)
    for attack in attack_order:
        # Remove the edge from the nodes of other side
        for other_node in attacked_graph[attack]:
            attacked_graph[other_node].discard(attack)
        # Remove all the edge of the node being attack
        attacked_graph.pop(attack)
    # Use BFS to calculate the sets of connected components for the final graph
    final_graph = cc_visited(attacked_graph)
    # groups <- group_nodes: set of connected nodes, node_root <- node:group node of its belonging group
    groups = dict()
    node_root = dict()
    # Create groups and node_root for the final graph
    for group in final_graph:
        # Set an arbitrary item from this group as group root
        for group_root in group:
            break
        groups[group_root] = set([group_root])
        for node in group:
            groups[group_root].add(node)
            node_root[node] = group_root
    # Compute the resilience of the final graph
    max_size = 0
    for root in groups:
        if len(groups[root]) > max_size:
            max_size = len(groups[root])
    resilience = [max_size]

    # Add the attacked node back and compute the resilience for each step
    attack_order_copy = attack_order[:]
    while len(attack_order_copy) != 0:
        new_node = attack_order_copy.pop()
        # Initialize the new node
        groups[new_node] = set([new_node])
        node_root[new_node] = new_node
        # Union the set of attacked node and the set of neighbor
        for neighbor in ugraph[new_node]:
            # If the neighbor is the node in the attack list (haven't be added back), skip
            if neighbor not in attack_order_copy:
                root_neighbor = node_root[neighbor]
                root_new_node = node_root[new_node]
                # Judge whether they are in the same group, if not, union two sets
                if root_neighbor != root_new_node:
                    for node in groups[root_new_node]:
                        # Path compression
                        node_root[node] = root_neighbor
                        # Union
                        groups[root_neighbor].add(node)
                    # Discard the original group of new_node
                    groups.pop(root_new_node)
        # Resilience for each iteration
        max_size = 0
        for root in groups:
            if len(groups[root]) > max_size:
                max_size = len(groups[root])
        resilience = [max_size] + resilience
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
    ugraph = SAMPLE.GRAPH7
    attack_order = [2, 0, 19, 20, 40, 13, 7, 6, 33, 45, 8]
    print compute_resilience(ugraph, attack_order)


def test_compute_resilience_disjoint_set():
    """
    Test 5 - compute_resilience_disjoint_set
    """
    ugraph = SAMPLE.GRAPH7
    attack_order = [2, 0, 19, 20, 40, 13, 7, 6, 33, 45, 8]
    print compute_resilience_disjoint_set(ugraph, attack_order)
#test_bfs_visited()
#test_cc_visited()
#test_largest_cc_size()
#test_compute_resilience()
