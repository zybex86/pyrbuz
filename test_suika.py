import unittest
import pymunk
import numpy as np

from suika import Particle, PreParticle, Wall, RADII, DENSITY, ELASTICITY, THICKNESS

class DummyMapper(dict):
    pass

class TestParticle(unittest.TestCase):
    def setUp(self):
        self.space = pymunk.Space()
        self.mapper = DummyMapper()

    def test_particle_creation(self):
        p = Particle((100, 100), 0, self.space, self.mapper)
        self.assertEqual(p.n, 0)
        self.assertEqual(p.radius, RADII[0])
        self.assertTrue(p.alive)
        self.assertIn(p.shape, self.mapper)
        self.assertIn(p.shape, self.space.shapes)

    def test_particle_kill(self):
        p = Particle((100, 100), 0, self.space, self.mapper)
        p.kill(self.space)
        self.assertFalse(p.alive)
        self.assertNotIn(p.shape, self.space.shapes)

    def test_particle_position(self):
        p = Particle((123, 456), 0, self.space, self.mapper)
        np.testing.assert_array_equal(p.pos, np.array([123, 456]))

class TestPreParticle(unittest.TestCase):
    def test_set_x_limits(self):
        pre = PreParticle(100, 0)
        pre.set_x(10)
        self.assertGreaterEqual(pre.x, 24 + RADII[0] + THICKNESS // 2)
        pre.set_x(1000)
        self.assertLessEqual(pre.x, 570 - (24 + RADII[0] + THICKNESS // 2))

class TestWall(unittest.TestCase):
    def setUp(self):
        self.space = pymunk.Space()

    def test_wall_creation(self):
        w = Wall((0, 0), (100, 100), self.space)
        self.assertIn(w.shape, self.space.shapes)
        self.assertEqual(w.shape.friction, 10)

if __name__ == "__main__":
    unittest.main()