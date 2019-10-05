from model.cube import Cube
import numpy as np

if __name__ == '__main__':
  c = Cube()
  index_table = np.load('index_table.npy')
  c.read_cube(index_table)
  print(c)
  print('rotating front face')
  c.rotate(0)
  print(c)
