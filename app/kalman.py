import numpy as np


class Kalman(object):
    def __init__(self, *, lat, lon, p=None, state=None):
        self.id = id
        self.lat = lat
        self.lon = lon

        self.T = 1  # time

        self.Q = np.matrix([[0.25, 0],
                            [0, 0.25]])

        self.R = np.matrix([[2.0, 0],
                            [0, 2.0]])

        self.H = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0]])

        self.F = np.matrix([[1, 0, self.T, 0],
                            [0, 1, 0, self.T],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        self.G = np.matrix([[0, 0],
                            [0, 0],
                            [1, 0],
                            [0, 1]])

        self.P = p
        self.I = np.eye(4)

        # self.init_state = np.matrix([lat, lon, 0, 0])
        self.state = state

        self.x_tr = np.array([])
        self.y_tr = np.array([])

    def count_current_state(self, *, lat, lon, P=None, state=None):
        new_state = self.F * self.state
        self.P = self.F * self.P * self.F.T + \
                 self.G * self.Q * self.G.T
        z_x = self.H * new_state
        z = np.matrix([lat, lon]).T
        e_x = z - z_x
        s_x = self.H * self.P * self.H.T + self.R
        k_x = self.P * self.H.T * np.linalg.inv(s_x)
        new_state_x = new_state + k_x * e_x
        self.P = (self.I - k_x * self.H) * self.P
        self.state = new_state_x
        place = self.state.T
        xx = place.item(0)
        yy = place.item(1)
        self.x_tr = np.append(self.x_tr, xx)
        self.y_tr = np.append(self.y_tr, yy)

        return self.P, self.state

