from alpha_vantage.timeseries import TimeSeries


class TickerError(Exception):
    def __init__(self, desc):
        desc = 'Manatee Ticker Error :: ' + desc
        super(TickerError, self).__init__(desc)


class TickerResult:

    def __init__(self):
        pass


class Ticker:

    def __init__(self, api_key='GBI5B3IH307H9BNZ'):
        self._api_key = api_key
        self._ts = None

        self._create_internal_endpoint()

    def _create_internal_endpoint(self):

        if not self._api_key:
            raise TickerError('Invalid API key')

        try:
            self._ts = TimeSeries(key=self._api_key)
        except ValueError as ve:
            raise TickerError('Internal error on TS creation %s' % str(ve))

    def get_data(self):

        res = TickerResult()

        data, metadata = self._ts.get_daily('SPX', outputsize='full')

        return res
