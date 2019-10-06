import numpy as np
from utils.zobrist import generate_zobrist
from utils.base import generate_base
import copy


class Cube():
  """Cube class defines a rubik's cube A ribuk's cube has six faces, Front(0 +x), Up(1 +y), Left(2 +z), Right(3 -z), Down(4 -y), Back(5 -x). Each face has nine colors. These colors are noted in a coordinate system. For example, the Botton center has the color of color_(0, 0, -2), and the grid on the bottom face that is adjacent to front- bottom edge has the color of (1, 0, -2).

  The rubik's cube is consider solved when all front color's 0, right
  color's 1, ...
  """

  def __init__(self):
    print("initializing cube...")
    self.zobrist_arr_ = generate_zobrist()
    # all of different bases:
    self.bases_ = generate_base()
    self.faces_ = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, -1],
        [0, -1, 0],
        [-1, 0, 0]], dtype=np.int8)
    self.variant_faces_ = np.zeros((48, 6, 3), dtype=np.int8)
    for idx, base in enumerate(self.bases_):
      self.variant_faces_[idx] = np.dot(self.faces_, base)
    # array of points. contains 54 points.
    self.index_arr_ = None
    self.color_ = np.ones((5, 5, 5), dtype=np.uint8)
    self.base_indices = []
    for y in range(-1, 2):
      for z in range(-1, 2):
        self.base_indices.append(np.array((2, y, z)))
    # rotation matrix:
    # [ cos(theta) -sin(theta)
    #   sin(theta)  cos(theta)]
    self.face_vectors = [
        np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
        np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),
        np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
        np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
        np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # rotate pi in the xy plane
    ]
    self.faces = []
    for v in self.face_vectors:
      face = []
      for idx in self.base_indices:
        face.append(np.dot(idx, v))
      self.faces.append(face)
    self.face_name = ["Front", "Up", "Left", "Right", "Down", "Back"]
    for idx, rot in enumerate(self.face_vectors):
      for base_index in self.base_indices:
        rotated_index = np.dot(base_index, rot)
        self.set_color(rotated_index, idx)
    # five unit grids to generate front face rotation points
    front_rot_quarter = np.array([[1, 2, -1], [1, 2, 0], [1, 2, 1], [2, 1, -1],
                                  [2, 1, 0]])
    front_rot_90 = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    front_rot_half = np.append(
        front_rot_quarter, np.dot(front_rot_quarter, front_rot_90), axis=0)
    # grids to rotate if rotating the front face.
    front_rot_from = np.append(
        front_rot_half,
        np.dot(np.dot(front_rot_half, front_rot_90), front_rot_90),
        axis=0)
    # point that front_rot_points will rotate to.
    front_rot_to = np.dot(front_rot_from, front_rot_90)
    # generate rotate from and rotate to from face vectors
    self.rotate_from = np.empty([6, 20, 3], dtype=np.int8)
    self.rotate_to = np.empty([6, 20, 3], dtype=np.int8)
    for idx, v in enumerate(self.face_vectors):
      self.rotate_from[idx] = np.dot(front_rot_from, v)
      self.rotate_to[idx] = np.dot(front_rot_to, v)
    self.create_index_arr()
    self.reset_cube()

  def set_color(self, point, color):
    p = point + 2
    self.color_[(p[0], p[1], p[2])] = color

  def get_color(self, point):
    p = point + 2
    return self.color_[(p[0], p[1], p[2])]

  # rotates a side (with center normal unit vector) clockwise
  # face is the face index number.
  def rotate(self, face):
    from_color = self.color_.copy()
    for from_pt, to_pt in zip(self.rotate_from[face], self.rotate_to[face]):
      from_idx = from_pt + 2
      self.set_color(to_pt, from_color[(from_idx[0], from_idx[1], from_idx[2])])
    self.update_zobrist()

  def __str__(self):
    res = ""
    for idx, name in enumerate(self.face_name):
      res += name.rjust(8, " ")
      res += ": "
      for base_index in self.base_indices:
        res += " " + str(
            self.get_color(np.dot(base_index, self.face_vectors[idx])))
      res += "\n"
    return str(self.color_)

  def copy(self):
    c = copy.copy(self)
    c.color_ = self.color_.copy()
    c.zobrist_ = self.zobrist_.copy()
    return c

  """Resets cube state: face X is all of color X."""
  def reset_cube(self):
    for idx, rot in enumerate(self.face_vectors):
      for base_idx in self.base_indices:
        rot_idx = np.dot(base_idx, rot)
        self.set_color(rot_idx, idx)
    self.update_zobrist()

  def read_cube(self, arr):
    for idx, rot in enumerate(self.face_vectors):
      for base_idx in self.base_indices:
        rot_idx = np.dot(base_idx, rot)
        p = rot_idx + 2
        self.set_color(rot_idx, arr[p[0], p[1], p[2]])
    self.update_zobrist()

  def create_index_arr(self):
    self.index_arr_ = np.zeros((54, 3), dtype=np.int8)
    index_arr_idx = 0
    for idx, rot in enumerate(self.face_vectors):
      for base_idx in self.base_indices:
        rot_idx = np.dot(base_idx, rot)
        self.index_arr_[index_arr_idx] = rot_idx
        index_arr_idx += 1
    self.variant_index_arr_ = np.zeros((48, 54, 3), dtype=np.int8)
    for idx, base in enumerate(self.bases_): # 48x3x3
      self.variant_index_arr_[idx] = np.dot(self.index_arr_, base)
    self.update_zobrist()

  def read_index_arr(self, index_arr):
    self.index_arr_ = index_arr
    self.variant_index_arr_ = np.zeros((48, 54, 3), dtype=np.int8)
    for idx, base in enumerate(self.bases_): # 48x3x3
      self.variant_index_arr_[idx] = np.dot(index_arr, base)

  def read_zobrist_arr(self, zobrist_arr):
    self.zobrist_arr_ = zobrist_arr

  """What does current color maps to if under the variant_face system(6x3)"""
  def get_color_dict(self, variant_face):
    # this can be pre calculated.
    d = {}
    for idx, p in enumerate(variant_face):
      d[self.get_color(p * 2)] = idx
    return d

  def save(self, fname):
    print('saving cube to: ', fname)
    np.save(fname, self.color_)

  def update_zobrist(self):
    self.zobrist_ = set()
    for variant_face, variant_index_arr in zip(self.variant_faces_, self.variant_index_arr_):
      d = self.get_color_dict(variant_face)
      zobrist = 0
      for idx, pt in enumerate(variant_index_arr):
        n = d[self.get_color(pt)]
        zobrist ^= n * self.zobrist_arr_[idx]
      self.zobrist_.add(zobrist)

  def __eq__(self, other):
    return len(self.zobrist_ & other.zobrist_) != 0
