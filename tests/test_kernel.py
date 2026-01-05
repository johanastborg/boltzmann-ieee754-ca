import unittest
import struct
from src.kernel import CollisionKernel

class TestCollisionKernel(unittest.TestCase):
    def setUp(self):
        self.kernel = CollisionKernel(chaos_factor=1.0)

    def test_roundoff_seed_extraction(self):
        # Test that we can extract a seed from a float
        val = 1.23456789
        seed = self.kernel._extract_roundoff_seed(val)
        self.assertIsInstance(seed, int)
        self.assertTrue(0 <= seed <= 0xFFFF)

    def test_roundoff_seed_sensitivity(self):
        # Test that slightly different floats yield different seeds
        val1 = 1.000000000000001
        val2 = 1.000000000000002
        seed1 = self.kernel._extract_roundoff_seed(val1)
        seed2 = self.kernel._extract_roundoff_seed(val2)

        # It's possible they collide, but unlikely for sequential small changes in mantissa
        self.assertNotEqual(seed1, seed2, "Seeds should differ for micro-variations in float value")

    def test_collide_output(self):
        cell = 10.0
        neighbors = [10.0, 10.0, 10.0, 10.0]
        result = self.kernel.collide(cell, neighbors)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)

    def test_multi_cell_collision_preserves_sum(self):
        # The multi_cell_collision method is designed to redistribute energy
        cells = [10.0, 20.0, 5.0]
        initial_sum = sum(cells)
        new_cells = self.kernel.multi_cell_collision(cells)
        final_sum = sum(new_cells)

        self.assertAlmostEqual(initial_sum, final_sum, places=7, msg="Energy should be conserved in multi_cell_collision")
        self.assertNotEqual(cells, new_cells, "Cells should have changed state")

if __name__ == '__main__':
    unittest.main()
