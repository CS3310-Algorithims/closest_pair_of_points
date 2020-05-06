import math
import random


def distance(point_a, point_b):
    """Find distance between two points where points are n-tuple"""
    return math.sqrt(sum((a - b)**2 for a, b in zip(point_a, point_b)))


def gen_unique_kd_points(n, dim):
    nd = [random.sample(range(-n*10, n*10), n) for d in range(dim)]
    return [p for p in zip(*nd)]


def min_of_pairs(pair_a, pair_b):
    """Return closest pair of Points of two pair of Points"""
    return pair_a if pair_a["distance"] <= pair_b["distance"] else pair_b
