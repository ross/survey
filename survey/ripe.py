#
#
#

from logging import getLogger

from requests import Session


class RipeClient:
    BASE_URL = 'https://atlas.ripe.net/api/v2'

    log = getLogger('RipeClient')

    def __init__(self, api_key=None):
        self.log.info('__init__: api_key=%s', '***' if api_key else None)
        sess = Session()
        if api_key is not None:
            sess.headers['authorization'] = f'Key {api_key}',
        sess.headers['user-agent'] = 'octodns/survey/0.1'
        self._sess = sess

        self._probe_cache = {}

    def _request(self, method, path):
        self.log.debug('_request: method=%s, path=%s', method, path)
        url = f'{self.BASE_URL}{path}'
        resp = self._sess.request(method, url)
        resp.raise_for_status()
        return resp.json()

    def probe(self, probe_id):
        self.log.debug('probe: probe_id=%s', probe_id)
        try:
            probe = self._probe_cache[probe_id]
            self.log.debug('probe:   cached')
            return probe
        except KeyError:
            pass

        self.log.debug('probe:   fetching')
        path = f'/probes/{probe_id}/'
        probe = self._request('GET', path)
        self._probe_cache[probe_id] = probe
        return probe

    def measurement(self, measurement_id):
        self.log.debug('measurement: measurement_id=%s', measurement_id)
        path = '/measurements/{}'.format(measurement_id)
        return self._request('GET', path)

    def measurement_results(self, measurement_id):
        self.log.debug(
            'measurement_results: measurement_id=%s',
            measurement_id,
        )
        path = '/measurements/{}/results/'.format(measurement_id)
        return self._request('GET', path)
