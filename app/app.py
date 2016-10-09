import os
import sys
import json

import numpy as np
from flask import Flask, request

from scoring_engine import ScoringEngine


SE = ScoringEngine()
app = Flask(__name__)


@app.route('/kalman/<track_id>', methods=['POST'])
def kalman(track_id):
    data = json.loads(request.data.decode("utf-8"))
    corrected_lat, corrected_lon = SE.calculate(data=data, id=track_id)
    return "{} {} \n".format(corrected_lat, corrected_lon)


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

