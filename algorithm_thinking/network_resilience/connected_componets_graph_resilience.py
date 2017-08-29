"""
Computing the set of connected components (CCs) of an undirected graph and determining the size of its largest connected componets
by implementing Breadth-first Search.
"""

from collections import deque
import undirected_graph_sample as SAMPLE
import copy
import random
import urllib2
import matplotlib.pyplot as plt
import time


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
    start_time = time.time()
    ugraph_copy = copy.deepcopy(ugraph)
    resilience = list()
    resilience.append(largest_cc_size(ugraph_copy))
    start_time = time.time()
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
    start_time = time.time()
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


def graph_loader(graph_url):
    """
    Loads graph from a given URL and represents it as a dict
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_dict = dict()
    count = 0
    for line in graph_file:
        line = line.split()
        count += 1
        graph_dict[int(line[0])] = set([int(head) for head in line[1:]])
    print "Loaded %d nodes in total" % count
    return graph_dict


def make_complete_graph(num_nodes):
    """
    Takes the number of nodes and returns a dictionary
    corresponding to a complete graph with the specified number of nodes.
    """
    graph_dict = dict()
    for node in xrange(num_nodes):
        graph_dict[node] = set([head for head in xrange(num_nodes) if head != node])
    return graph_dict


def make_UER_graph(nodes_num, p_value):
    """
    Use ER method to create an undirected graph based on the given number of nodes
    and the possibility of each edge, return a dict
    """
    graph_dict = {node:set([]) for node in xrange(nodes_num)}
    for head in xrange(nodes_num):
        for tail in xrange(head + 1, nodes_num):
            if random.random() < p_value:
                graph_dict[head].add(tail)
                graph_dict[tail].add(head)
    return graph_dict


class UPATrial:
    """
    Simple class to encapsulate optimized trials for UPA algorithm

    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities, which is changed
    during each subtrial.

    Uses random.choice() to select a node number from this list for each trial.
    """
    def __init__(self, nodes_num):
        """
        Initialize a UPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._node_num = nodes_num
        self._node_space = [node for node in xrange(nodes_num) for dummy_idx in xrange(nodes_num)]

    def run_trial(self, nodes_choose):
        """
        Conduct num_node trials by using applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities

        Returns:
        Set of nodes
        """
        neighbor_set = set([])
        for dummy_idx in xrange(nodes_choose):
            neighbor_set.add(random.choice(self._node_space))
        self._node_space.extend(list(neighbor_set))
        self._node_space.extend([self._node_num] * (len(neighbor_set) + 1))
        self._node_num += 1
        return neighbor_set


def make_UPA_graph(nodes_num, nodes_choose):
    """
    Use UPA method to create a random directed graph based on the given final_nodes and nodes_choose in
    each iteration

    DPA - Undirected graph with Preferential Attachment
    """
    graph_dict = make_complete_graph(nodes_choose)
    trial = UPATrial(nodes_choose)
    for node in xrange(nodes_choose, nodes_num):
        neighbors = trial.run_trial(nodes_choose)
        graph_dict[node] = neighbors
        for neighbor in neighbors:
            graph_dict[neighbor].add(node)
    return graph_dict


def random_order(ugraph):
    """
    Takes a dict of an undirected graph,
    return an list of all nodes in random random_order
    """
    order = ugraph.keys()
    random.shuffle(order)
    return order


def compare_resilience(resilience_list, graphs_name):
    """
    Use line plot to compare the resilience of different type of graph
    """
    global TOTAL_NODES
    for graph_index in xrange(len(resilience_list)):
        plt.plot(range(TOTAL_NODES + 1), resilience_list[graph_index], label=graphs_name[graph_index])
    plt.title('The Resilience of Three Types of Graph')
    plt.xlabel('Number of Nodes Removed')
    plt.ylabel('Maximum Size of Connected Nodes')
    plt.legend()
    plt.show()


def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph


def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


def fast_targeted_order(ugraph):
    """
    An Asymptotically faster implemention of targeted_order
    Stored nodes group by it's degree, and iterate them descending
    """
    new_graph = copy_graph(ugraph)
    DegreeSet = dict()
    nodes_num = len(ugraph)
    # Create Degree Set - DegreeSet[k] is a set of all nodes whose degree is k
    for degree in xrange(nodes_num):
        DegreeSet[degree] = set([])
    for node in new_graph:
        degree = len(new_graph[node])
        DegreeSet[degree].add(node)

    order = list()
    for degree in xrange(nodes_num - 1, -1, -1):
        while len(DegreeSet[degree]) > 0:
            target = DegreeSet[degree].pop()
            for neighbor in new_graph[target]:
                neighbor_degree = len(new_graph[neighbor])
                DegreeSet[neighbor_degree].remove(neighbor)
                DegreeSet[neighbor_degree - 1].add(neighbor)
            order.append(target)
            delete_node(new_graph, target)
    return order


def test_make_UER_graph():
    """
    TEST - make_UER_graph
    """
    print make_UER_graph(4, 1)
    print make_UER_graph(4, 0)
    print make_UER_graph(5, 0.5)


def test_make_UPA_graph():
    """
    TEST - make_UPA_graph
    """
    print make_UPA_graph(10, 3)

#test_make_UPA_graph()

# Question 1
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
COMPUTER_NETWORK = graph_loader(NETWORK_URL)
TOTAL_NODES = len(COMPUTER_NETWORK)
TOTAL_EDGES = sum([len(COMPUTER_NETWORK[node]) for node in COMPUTER_NETWORK]) / 2
P_VALUE = TOTAL_EDGES * 1.0 / (TOTAL_NODES * (TOTAL_NODES - 1) / 2)
P_VALUE = round(P_VALUE, 3)
AVERAGE_EDGES = TOTAL_EDGES / TOTAL_NODES
UER_graph = make_UER_graph(TOTAL_NODES, P_VALUE)
UPA_graph = make_UPA_graph(TOTAL_NODES, AVERAGE_EDGES)

# ATTACK_ORDER_NETWORK = random_order(COMPUTER_NETWORK)
# NETWORK_RESILIENCE = compute_resilience_disjoint_set(COMPUTER_NETWORK, ATTACK_ORDER_NETWORK)
# ATTACK_ORDER_UER = random_order(UER_graph)
# UER_RESILIENCE = compute_resilience_disjoint_set(UER_graph, ATTACK_ORDER_UER)
# ATTACK_ORDER_UPA = random_order(UPA_graph)
# UPA_RESILIENCE = compute_resilience_disjoint_set(UPA_graph, ATTACK_ORDER_UPA)

# compare_resilience([NETWORK_RESILIENCE, UER_RESILIENCE, UPA_RESILIENCE], ['Network', 'ER p=0.004', 'UPA m=2'])


# Question 3
# O(n^2), O(n)
def solve_q3():
    run_time_standard = []
    run_time_fast = []
    for nodes_num in range(10, 1000, 10):
        UPAgraph = make_UPA_graph(nodes_num, 5)
        start_time = time.time()
        result = targeted_order(UPAgraph)
        end_time = time.time()
        run_time_standard.append(end_time - start_time)
        start_time = time.time()
        fast_result = fast_targeted_order(UPAgraph)
        end_time = time.time()
        run_time_fast.append(end_time - start_time)

    plt.plot(range(10, 1000, 10), run_time_standard, label='targeted_order')
    plt.plot(range(10, 1000, 10), run_time_fast, label='fast_targeted_order')
    plt.legend()
    plt.title('The Running Time of Two Target Order Methods - Desktop Python')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Running Time (seconds)')
    plt.show()


# Question 4
def solve_q4():
    attack_order_network = fast_targeted_order(COMPUTER_NETWORK)
    attack_order_UER = fast_targeted_order(UER_graph)
    attack_order_UPA = fast_targeted_order(UPA_graph)
    network_resilience = compute_resilience_disjoint_set(COMPUTER_NETWORK, attack_order_network)
    UER_resilience = compute_resilience_disjoint_set(UER_graph, attack_order_UER)
    UPA_resilience = compute_resilience_disjoint_set(UPA_graph, attack_order_UPA)
    compare_resilience([network_resilience, UER_resilience, UPA_resilience], ['Network', 'ER p=0.004', 'UPA m=2'])

solve_q4()
