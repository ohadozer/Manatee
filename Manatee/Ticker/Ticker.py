from os.path import dirname, abspath, join
from alpha_vantage.timeseries import TimeSeries


class TickerError(Exception):
    
    def __init__(self, desc):
        desc = 'Manatee Ticker Error :: ' + desc
        super(TickerError, self).__init__(desc)


class TickerResult:

    def __init__(self):
        pass


class Ticker:

    def __init__(self, api_key=None):

        if api_key:
            self._api_key = api_key
        else:
            try:
                key = join(dirname(abspath(__file__)), 'key.txt')
                self._api_key = open(key).read().split("\n")[0]
            except Exception as ex:
                raise TickerError('Error reading API key. %s' % str(ex))

        self._ts = None

        self._create_internal_endpoint()

    def _create_internal_endpoint(self):

        if not self._api_key:
            raise TickerError('Invalid API key')

        try:
            self._ts = TimeSeries(key=self._api_key)
        except ValueError as ve:
            raise TickerError('Internal error on TS creation. %s' % str(ve))

    def get_data(self):

        res = TickerResult()

        data, metadata = self._ts.get_daily('SPX', outputsize='full')

        return res
