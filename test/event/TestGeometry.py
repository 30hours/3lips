import unittest
from algorithm.geometry.Geometry import Geometry

class TestGeometry(unittest.TestCase):

    def test_lla2ecef(self):
        # Test case 1
        result = Geometry.lla2ecef(-34.9286, 138.5999, 50)
        self.assertAlmostEqual(result[0], -3926830.77177051, places=3)
        self.assertAlmostEqual(result[1], 3461979.19806774, places=3)
        self.assertAlmostEqual(result[2], -3631404.11418915, places=3)

        # Test case 2
        result = Geometry.lla2ecef(0, 0, 0)
        self.assertAlmostEqual(result[0], 6378137.0, places=3)
        self.assertAlmostEqual(result[1], 0, places=3)
        self.assertAlmostEqual(result[2], 0, places=3)

        # Add more test cases as needed

    def test_ecef2lla(self):
        # Test case 1
        result = Geometry.ecef2lla(-3926830.77177051, 3461979.19806774, -3631404.11418915)
        self.assertAlmostEqual(result[0], -34.9286, places=4)
        self.assertAlmostEqual(result[1], 138.5999, places=4)
        self.assertAlmostEqual(result[2], 50, places=3)

        # Test case 2
        result = Geometry.ecef2lla(6378137.0, 0, 0)
        self.assertAlmostEqual(result[0], 0, places=4)
        self.assertAlmostEqual(result[1], 0, places=4)
        self.assertAlmostEqual(result[2], 0, places=3)

if __name__ == '__main__':
    unittest.main()
