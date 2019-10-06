# Lint as: python3
"""Tests for cube."""
import unittest
from model.cube import Cube


class CubeTest(unittest.TestCase):
  def testSameCube(self):
    cube = Cube()
    new_cube = cube.copy()
    self.assertEqual(cube, new_cube)
    cube.rotate(0)
    self.assertNotEqual(cube, new_cube)
    new_cube.rotate(1)
    self.assertEqual(cube, new_cube)
    cube.rotate(0)
    self.assertNotEqual(cube, new_cube)
    new_cube.rotate(1)
    self.assertEqual(cube, new_cube)


if __name__ == '__main__':
  unittest.main()
