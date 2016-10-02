from flask import Flask
import os
import sys
import numpy as np

app = Flask(__name__)


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
    return "Numpy array: {}".format(int(z))

if __name__ == '__main__':
    # Get port from environment variable or choose 9099 as local default
    port = int(os.getenv("PORT", 9099))
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port, debug=True)

