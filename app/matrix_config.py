import numpy as np
# TODO: refactor this to make JSON config or DICT

T = 1

Q = np.matrix([[0.25, 0],
               [0, 0.25]])

R = np.matrix([[0.25, 0],
               [0,    0.25]])

H = np.matrix([[1, 0, 0, 0],
               [0, 1, 0, 0]])

F = np.matrix([[1, 0, T, 0],
               [0, 1, 0, T],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])

G = np.matrix([[0, 0],
               [0, 0],
               [1, 0],
               [0, 1]])

I = np.eye(4)
