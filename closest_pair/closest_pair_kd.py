"""
Closest Pair of Points in kth dimension
    - closest_pair_kd: Divide and Conquer in kth dimensions
    - bf_closest_pair_kd: Brute force in kth dimensions
"""
from .utils import distance, min_of_pairs


def bf_closest_pair_kd(points):
    """
    Bruteforce approach to get minimal distance of two points at kth dimensions.

    Parameters
    ----------
    points (list): List of tuple of kth dimensions.

    Return
    ------
    {"distance": float, "pair": Point}
    """
    n = len(points)

    if n < 2:
        raise IndexError()

    min_dist = distance(points[0], points[1])
    min_points = (points[0], points[1])

    for i in range(n - 1):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])

            if dist < min_dist:
                min_dist = dist
                min_points = (points[i], points[j])

    return {"distance": min_dist, "pair": min_points}


def bf_pairlist_kd(points):
    """
    Generate all bruteforce combinations for pairs.

    Parameters
    ----------
    points (list): List of tuple of kth dimensions.

    Return
    ------
    {"distance": float, "pair": Point}
    """
    n = len(points)
    pairs = []

    if n < 2:
        raise IndexError()

    min_dist = distance(points[0], points[1])
    min_points = (points[0], points[1])

    for i in range(n - 1):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            dist = distance(points[i], points[j])
            pairs.append((points[i], points[j], dist))

    return pairs


def closest_pair_kd(points):
    """
    Find closest pair in points using divide and conquer at kth dimensions.

    Timsort: O(nlogn)
    Closest: O(nlogn)
    Time Complexity: O(nlogn)

    Parameters
    ----------
    points (list): List of tuple of kth dimensions.

    Return
    ------
    {"distance": float, "pair": Point}
    """
    dim = len(points[0])

    # presort points by each coordinates up to k dimensions
    points_kd = [sorted(points, key=lambda p: p[d]) for d in range(dim)]

    return closest_kd(points_kd, dim, 0)


def closest_kd(points_kd, dim, level):
    """
    Recursively find the closest pair of points at the kth dimensions.
    Uses both direct recursion and indirect recursion from strip_closest_kd().

    Recurrence relation
    -------------------
    T(n, k) = 2T(n/2, k) + T(m, k-1) + O(n)
    m <= n/(logn)^(k-2) where m is the number of points by sparsity
    T(m, k-1) = O(m (logm)^(k-2) ) = O(n)
    T(n, k) = 2T(n/2, k) + O(n) + O(n) = O(nlogn)

    Time Complexity: O(nlogn)

    Parameters
    ----------
    points_kd (list): d x n array of tuple in max d dimensions.
    dim (int): Max dimension of points
    level: Kth dimension level with base of 0

    Return
    ------
    {"distance": float, "pair": Point}
    """
    n = len(points_kd[level])

    # base case: use brute force on size 3 or less
    if n <= 3:
        return bf_closest_pair_kd(points_kd[level])

    # get median point
    mid = n // 2
    med = points_kd[level][mid-1]
    points_left = [[] for d in range(dim)]
    points_right = [[] for d in range(dim)]

    # divide points
    for d in range(dim):
        if d == level:
            points_left[d] = points_kd[level][:mid]
            points_right[d] = points_kd[level][mid:]
        else:
            for point in points_kd[d]:
                if point[level] <= med[level]:
                    points_left[d].append(point)
                else:
                    points_right[d].append(point)

    # recursion
    min_left = closest_kd(points_left, dim, level)
    min_right = closest_kd(points_right, dim, level)
    min_pair = min_of_pairs(min_left, min_right)

    # create strip
    delta = min_pair['distance']
    strip = [[p for p in points_kd[d] if abs(med[level] - p[level]) < delta]
             for d in range(dim)]

    if level + 1 < dim:
        return strip_closest_kd(strip, min_pair, dim, level + 1)
    else:
        return strip_closest_kd(strip, min_pair, dim, level)


def strip_closest_kd(strip, min_pair, dim, level):
    """
    Find any points smaller than min_pair with given stirp array.
    Indirect recursion to closest_kd().

    Parameters
    ----------
    strip (list): d x n array of tuple in max d dimensions.
    min_pair (dict): Minimal pair of points with key 'distance' and 'pair'.
    dim (int): Max dimension of points
    level: Kth dimension level

    Return
    ------
    {"distance": float, "pair": Point}
    """
    # recursion into strip if next level is less then dimension
    if level + 1 < dim and len(strip[level]) > 1:
        level_min = closest_kd(strip, dim, level)
        min_pair = min_of_pairs(min_pair, level_min)

    # try to find a smaller min_pair in strip
    for i in range(len(strip[level]) - 1):
        for j in range(i + 1, min(i + 7, len(strip[level]))):
            dist = distance(strip[level][i], strip[level][j])

            if dist < min_pair['distance']:
                min_pair['distance'] = dist
                min_pair['pair'] = (strip[level][i], strip[level][j])

    return min_pair
