import numpy as np
import matplotlib.pyplot as plt


class Kalman(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

        self.P = 5 * np.eye(4)
        self.I = np.eye(4)

        self.init_state = np.matrix([x.item(0), y.item(0), 0, 0])
        self.state = self.init_state.T

        self.x_tr = np.array([])
        self.y_tr = np.array([])

    def count_current_state(self, i):
        new_state = self.F * self.state
        self.P = self.F * self.P * self.F.T + \
                 self.G * self.Q * self.G.T
        z_x = self.H * new_state
        z = np.matrix([x.item(i + 1), y.item(i + 1)]).T
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


def read_data(file_name):
    with open(file_name, 'r') as data:
        x, y = [], []
        for line in data:
            line = line.split(' ')
            x_value = line[0]
            y_value = line[1]
            y_value = y_value.replace('\n', '')
            x.append(float(x_value))
            y.append(float(y_value))
    return np.matrix(x), np.matrix(y)


if __name__ == "__main__":
    x, y = read_data("data.txt")
    kalman = Kalman(x, y)
    for i in range(500):
        kalman.count_current_state(i)
    x = np.squeeze(np.asarray(x))
    y = np.squeeze(np.asarray(y))
    a = kalman.x_tr
    b = kalman.y_tr
    plt.plot(a,b,x,y)
    plt.show()
