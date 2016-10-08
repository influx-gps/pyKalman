import requests
import time
import json
import numpy as np
import matplotlib.pyplot as plt


def read_data(file_name):
    with open(file_name, 'r') as data:
        for line in data:
            line = line.split(' ')
            x_value, y_value = line[0], line[1]
            y_value = y_value.replace('\n', '')
            yield float(x_value), float(y_value)


def send_data():
    for each in read_data("data.txt"):
        payload = {'lat': each[0], 'lon': each[1]}
        r = requests.post('http://localhost:5000/1', data=json.dumps(payload))
        time.sleep(0.01)
        with open("filterd.txt", "a") as file:
            file.write(r.text)
        print(r.text)


if __name__ == "__main__":
    # send_data()
    x = []
    y = []
    for a, b in read_data("data.txt"):
        x.append(a)
        y.append(b)

    v = []
    z = []
    for a, b in read_data("filterd.txt"):
        v.append(a)
        z.append(b)

    x = np.squeeze(np.asarray(x))
    y = np.squeeze(np.asarray(y))

    v = np.squeeze(np.asarray(v))
    z = np.squeeze(np.asarray(z))

    plt.plot(x, y, v, z)
    plt.show()