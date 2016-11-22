import numpy as np
from matrix_config import T, Q, R, H, F, G, I


class Kalman(object):
    def __init__(self):
        self.T = T
        self.Q = Q
        self.R = R
        self.H = H
        self.F = F
        self.G = G
        self.I = I

    def estimate(self, lat, lon, P, state):
        new_state = self.F * state
        P = self.F * P * self.F.T + \
                 self.G * self.Q * self.G.T
        z_x = self.H * new_state
        z = np.matrix([lat, lon]).T
        e_x = z - z_x
        s_x = self.H * P * self.H.T + self.R
        k_x = P * self.H.T * np.linalg.inv(s_x)
        new_state_x = new_state + k_x * e_x
        P = (self.I - k_x * self.H) * P
        state = new_state_x
        place = state.T
        xx = place.item(0)
        yy = place.item(1)

        return P, state, xx, yy

