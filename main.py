from model.cube import Cube
from solver.solver import Solver
import numpy as np
from utils.read_cube import read_cube_arr

if __name__ == '__main__':
  c = Cube()
  color = 'gyrgggbbb boyyybrrb obwyryooo yrgrowrgy wwwwwowwr gggobrybo'
  arr = read_cube_arr(color)
  print(arr)
  c.read_cube(arr)
  s = Solver(c)
  s.solve()
  print(s.solution)
