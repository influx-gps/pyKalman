import os
import sys
import time
import json

import requests
import numpy as np
import matplotlib.pyplot as plt

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.DEBUG)


DATA_FILE = "data.txt"
FILTER_DATA_TEMP = "filter.txt"
DEFAULT_HOST = 'http://localhost:9099/kalman/1'


def read_data(*, filename):
    with open(filename, 'r') as data:
        for line in data:
            line = line.split(' ')
            x_value, y_value = line[0], line[1]
            y_value = y_value.replace('\n', '')
            yield float(x_value), float(y_value)


def send_data(*, datafile, host=DEFAULT_HOST):
    data = init_transmission(datafile=datafile)
    for each in data:
        payload = {'lat': each[0], 'lon': each[1], 'position': 'CONTINUE'}
        r = requests.post(host, data=json.dumps(payload))
        with open(FILTER_DATA_TEMP, "a+") as file:
            file.write(r.text)


def init_transmission(*, datafile):
    data = read_data(filename=datafile)
    init_lat, init_lon = next(data)
    payload = {'lat': init_lat, 'lon': init_lon, 'position': 'START'}
    r = requests.post(host, data=json.dumps(payload))
    with open(FILTER_DATA_TEMP, "a+") as file:
        file.write(r.text)
    return data


def clean():
    os.remove(FILTER_DATA_TEMP)


if __name__ == "__main__":
    logging.info("Start sending data.")

    try:
        host = sys.argv[1]
    except IndexError:
        logging.debug("Working in local mode.")
        host = DEFAULT_HOST
    try:
        send_data(datafile=DATA_FILE, host=host)

        logging.info("Creating vectors.")
        x, y = zip(*[(lat, lon) for lat, lon in read_data(filename=DATA_FILE)])
        x = np.squeeze(np.asarray(x))
        y = np.squeeze(np.asarray(y))

        v, z = zip(*[(lat, lon) for lat, lon in read_data(filename=FILTER_DATA_TEMP)])
        v = np.squeeze(np.asarray(v))
        z = np.squeeze(np.asarray(z))

        logging.info("Plotting tracks.")
        plt.plot(x, y, v, z)
        plt.show()
    finally:
        logging.info("Performing clean-up.")
        clean()
