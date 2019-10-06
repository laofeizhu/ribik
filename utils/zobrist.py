import random
import numpy as np

def generate_zobrist():
  a = np.zeros(54, dtype=np.int64)
  MAX60 = 0xfffffffffffffff
  for i in range(54):
    a[i] = random.randint(0, MAX60)
  return a
