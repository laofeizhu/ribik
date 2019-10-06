import numpy as np


"""Generates a 3x3 matrx where each column is the unit vector of new base"""
def generate_base():
  bases = np.array([
      [1, 0, 0],
      [-1, 0, 0],
      [0, 1, 0],
      [0, -1, 0],
      [0, 0, 1],
      [0, 0, -1]], dtype = np.int8)
  new_base = []
  for x in range(6):
    for y in range(6):
      for z in range(6):
        tmp = np.array([bases[x], bases[y], bases[z]], dtype = np.int8)
        if np.linalg.det(tmp) != 0:
          new_base.append(np.transpose(tmp))
  return np.asarray(new_base, dtype = np.int8)
