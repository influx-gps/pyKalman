import requests
import time
import json


def read_data(file_name):
    with open(file_name, 'r') as data:
        for line in data:
            line = line.split(' ')
            x_value, y_value = line[0], line[1]
            y_value = y_value.replace('\n', '')
            yield float(x_value), float(y_value)

if __name__ == "__main__":
    for each in read_data("data.txt"):
        payload = {'lat': each[0], 'lon': each[1]}
        r = requests.post('http://localhost:5000/1', data=json.dumps(payload))
        time.sleep(3)
        print(r.text)
