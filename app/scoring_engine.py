from collections import namedtuple
import numpy as np

from kalman import Kalman


class ScoringEngine(object):
    def __init__(self):
        self._cache = {}
        self._Record = namedtuple('Record', 'lat lon P state')

    def calculate(self, data, id):
        lat, lon, position = ScoringEngine.unpack_request(request_data=data)
        p_m, state = self._get_factors(position=position, id=id, lat=lat, lon=lon)
        result = Kalman().estimate(lat=float(lat), lon=float(lon), P=p_m, state=state)
        p_m, state, corrected_lat, corrected_lon = result
        self._update_record(id=id, lat=lat, lon=lon, P=p_m, state=state)
        return str(corrected_lat), str(corrected_lon)

    def _get_factors(self, position, id, lat, lon):
        if position == "START":
            return self._init_params(id=id, lat=lat, lon=lon)
        return self._get_last_params(id=id)

    def _init_params(self, id, lat, lon):
        init_state = np.matrix([lat, lon, 0, 0])
        state = init_state.T
        P = 5 * np.eye(4)
        self._cache[id] = self._Record(lat, lon, P, state)
        return P, state

    def _get_last_params(self, id):
        last_record = self._cache.get(id)
        return last_record.P, last_record.state

    def _update_record(self, id, lat, lon, P, state):
        self._cache[id] = self._Record(lat, lon, P, state)

    @staticmethod
    def unpack_request(request_data):
        lat = request_data["latitude"]
        lon = request_data["longitude"]
        position = request_data["position"]
        return lat, lon, position
