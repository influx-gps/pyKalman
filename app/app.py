import os
import sys
import json
from collections import namedtuple

import numpy as np
from flask import Flask, request

from kalman import Kalman

CACHE_STATE = {}
Record = namedtuple('Record', 'lat lon P state')
app = Flask(__name__)


def init_params(*, id, lat, lon):
    init_state = np.matrix([lat, lon, 0, 0])
    state = init_state.T
    P = 5 * np.eye(4)
    CACHE_STATE[id] = Record(lat, lon, P, state)
    return P, state


def get_last_params(*, id):
    last_record = CACHE_STATE.get(id)
    return last_record.P, last_record.state


@app.route('/kalman/<track_id>', methods=['POST'])
def kalman(track_id):
    data = json.loads(request.data.decode("utf-8"))
    lat = data["lat"]
    lon = data["lon"]
    position = data["position"]

    p_m, state = init_params(id=track_id, lat=lat, lon=lon) \
        if position == "START" \
        else get_last_params(id=track_id)

    km = Kalman(lat=lat, lon=lon, p=p_m, state=state)
    p_m, state = km.count_current_state(lat=float(lat), lon=float(lon))

    CACHE_STATE[track_id] = Record(lat, lon, p_m, state)

    return "{} {} \n".format(str(km.x_tr[-1]), str(km.y_tr[-1]))


@app.route('/')
def root():
    python_version = "\npython-version%s\n" % sys.version
    r = """<br><br>
    Kalman API<br>
    Bachelor Thesis /all.<br>"""
    return python_version + r


@app.route('/numpy')
def test_numpy():
    z = np.array([1729])
    return """"<br><br>
    Numpy Test<br>
    This endpoint checks if env has installed numpy.<br>
    Test value = {}""".format(int(z))

if __name__ == '__main__':
    # Get port from environment variable or choose 9099 as local default
    port = int(os.getenv("PORT", 9099))
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port, debug=True)

