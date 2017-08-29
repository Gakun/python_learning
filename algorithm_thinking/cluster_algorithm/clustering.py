"""
Method for finding closest pair and clustering data
"""
#import cluster_class as alg_cluster


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
    Input: list of Cluster objects
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
