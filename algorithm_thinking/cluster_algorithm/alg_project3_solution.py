"""
Method for finding closest pair and clustering data
"""
import alg_cluster


def slow_closest_pair(cluster_list):
    """
    Input: list of Cluster objects
    Return: tuple (dist, idx1, idx2)
    Brute Force
    """
    min_distance = float('inf')
    min_index1 = 0
    min_index2 = 0
    for idx1 in xrange(len(cluster_list)):
        for idx2 in xrange(idx1 + 1, len(cluster_list)):
            dist = cluster_list[idx1].distance(cluster_list[idx2])
            if dist < min_distance:
                min_distance = dist
                min_index1 = idx1
                min_index2 = idx2
    return (min_distance, min_index1, min_index2)


def fast_closest_pair(cluster_list):
    """
    Input: list of Cluster objects, sorted by horiz_center of each cluster
    Return: tuple (dist, idx1, idx2)
    Divided and conquer
    """
    size = len(cluster_list)
    if size <= 3:
        result = slow_closest_pair(cluster_list)
    else:
        mid = size / 2
        result_left = fast_closest_pair(cluster_list[:mid])
        result_right = fast_closest_pair(cluster_list[mid:])
        result_right = (result_right[0], result_right[1] + mid, result_right[2] + mid)
        if result_left[0] <= result_right[0]:
            result = result_left
        else:
            result = result_right
        center = (cluster_list[mid - 1].horiz_center() + cluster_list[mid].horiz_center()) / 2
        result_across = closest_pair_strip(cluster_list, center, result[0])
        if result_across[0] < result[0]:
            result = result_across
    return result


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Takes a list of Cluster object and two floats horiz_center, half_width,
    return the closest pair of clusters that lie in the spacified strip.
    """
    strip_indexs = [index for index in xrange(len(cluster_list)) if cluster_list[index].horiz_center() >= (horiz_center - half_width) \
    and cluster_list[index].horiz_center() <= (horiz_center + half_width)]
    strip_indexs.sort(key=lambda index: cluster_list[index].vert_center())
    size = len(strip_indexs)
    min_distance = float('inf')
    min_index1 = -1
    min_index2 = -1
    for idx1 in range(size - 1):
        for idx2 in range(idx1 + 1, min(idx1 + 4, size)):
            dist = cluster_list[strip_indexs[idx1]].distance(cluster_list[strip_indexs[idx2]])
            if dist < min_distance:
                min_distance = dist
                min_index1 = strip_indexs[idx1]
                min_index2 = strip_indexs[idx2]
    if min_index1 <= min_index2:
        return (min_distance, min_index1, min_index2)
    else:
        return (min_distance, min_index2, min_index1)


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Takes a list of Cluster objects and applies hierarchical clustering method,
    return the list of clusters
    """
    cluster_list_copy = cluster_list[:]
    while len(cluster_list_copy) > num_clusters:
        cluster_list_copy.sort(key=lambda cluster: cluster.horiz_center())
        pair = fast_closest_pair(cluster_list_copy)
        cluster_list_copy[pair[1]].merge_clusters(cluster_list_copy[pair[2]])
        cluster_list_copy.pop(pair[2])
    return cluster_list_copy


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Takes a list of Cluster objects and applies k-means clustering method,
    return this list of clusters.
    """
    clusters = list(cluster_list)
    clusters.sort(key=lambda cluster: cluster.total_population(), reverse=True)
    clusters = clusters[:num_clusters]
    for dummy_loop in xrange(num_iterations):
        new_clusters = [alg_cluster.Cluster(set(),0,0,0,0) for dummy_idx in range(num_clusters)]
        for county in cluster_list:
            min_index = -1
            min_distance = float('inf')
            for index in range(len(clusters)):
                distance = county.distance(clusters[index])
                if distance < min_distance:
                    min_distance = distance
                    min_index = index
            new_clusters[min_index].merge_clusters(county)
        clusters = new_clusters
    return clusters

