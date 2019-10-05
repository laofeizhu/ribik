import numpy as np


class Cube():
  """Cube class defines a rubik's cube A ribuk's cube has six faces, Front(0 +x), Up(1 +y), Left(2 +z), Right(3 -z), Down(4 -y), Back(5 -x). Each face has nine colors. These colors are noted in a coordinate system. For example, the Botton center has the color of color_(0, 0, -2), and the grid on the bottom face that is adjacent to front- bottom edge has the color of (1, 0, -2).

  The rubik's cube is consider solved when all front color's 0, right
  color's 1, ...
  """

  def __init__(self):
    print("initializing cube...")
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
      from_pt += 2
      self.set_color(to_pt, from_color[(from_pt[0], from_pt[1], from_pt[2])])

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

  """
  arr = np.array([[[ 1  1  1  1  1]
  [ 1 51 52 53  1]
  [ 1 48 49 50  1]
  [ 1 45 46 47  1]
  [ 1  1  1  1  1]]

 [[ 1  9 10 11  1]
  [18  1  1  1 29]
  [21  1  1  1 32]
  [24  1  1  1 35]
  [ 1 42 43 44  1]]

 [[ 1 12 13 14  1]
  [19  1  1  1 28]
  [22  1  1  1 31]
  [25  1  1  1 34]
  [ 1 39 40 41  1]]

 [[ 1 15 16 17  1]
  [20  1  1  1 27]
  [23  1  1  1 30]
  [26  1  1  1 33]
  [ 1 36 37 38  1]]

 [[ 1  1  1  1  1]
  [ 1  0  1  2  1]
  [ 1  3  4  5  1]
  [ 1  6  7  8  1]
  [ 1  1  1  1  1]]])

  """
  def read_cube(self, arr):
    for idx, rot in enumerate(self.face_vectors):
      for base_idx in self.base_indices:
        rot_idx = np.dot(base_idx, rot)
        p = rot_idx + 2
        self.set_color(rot_idx, arr[p[0], p[1], p[2]])





