import queue
import numpy as np
from model.cube import Cube
from datetime import datetime

def is_same(seta, setb):
  return len(seta & setb) != 0

class Solver():
  def __init__(self, c):
    self.target_ = c.copy()
    self.visited_ = set()
    self.moves_ = np.arange(6)

  def solve(self):
    init_cube = self.target_.copy()
    init_cube.reset_cube()
    q=queue.Queue()
    init_state = {'cube': init_cube, 'steps' :[]}
    q.put(init_state)
    total_steps = 0
    while not q.empty():
      total_steps += 1
      print('searching steps: ', total_steps)
      print('number of states visited: ', len(self.visited_))
      size = q.qsize()
      p = 0
      time = datetime.now()
      for n in range(size):
        new_p = int(n * 100 / size)
        if new_p > p:
          print('finished percentage: ', new_p)
          p = new_p
          time_now = datetime.now()
          print('elapsed time: ', time_now - time)
          time = time_now
        state = q.get()
        cube = state['cube']
        for move in self.moves_:
          new_cube = cube.copy()
          new_cube.rotate(move)
          new_steps = state['steps'].copy()
          new_steps.append(move)
          if is_same(new_cube.zobrist_, self.target_.zobrist_):
            print('new cube is the same as target cube, solution found')
            self.solution = new_steps
            return
          if is_same(new_cube.zobrist_, self.visited_):
            continue
          self.visited_ = set(self.visited_ | new_cube.zobrist_)
          new_state = {'cube': new_cube, 'steps': new_steps}
          q.put(new_state)



