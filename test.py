"""
All unit tests
"""
import unittest
from tests import closest_pair_points


MODULES = [
    closest_pair_points
]


class Test(unittest.TestCase):
    """
    Run all tests
    """
    for module in MODULES:
        suite = unittest.TestLoader().loadTestsFromModule(module)
        unittest.TextTestRunner(verbosity=2).run(suite)
