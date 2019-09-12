from os.path import dirname, abspath, join
from alpha_vantage.timeseries import TimeSeries
from enum import Enum

class TickerError(Exception):

    def __init__(self, desc):
        desc = 'Manatee Ticker Error :: ' + desc
        super(TickerError, self).__init__(desc)

class TickerResultTimeFrame(Enum):
    Daily = 1
    Weekly = 1
    Monthly = 3
    Yearly = 4

class TickerResult:

    def __init__(self):
        self._tf = TickerResultTimeFrame.Daily
        self._data = {}


class Ticker:

    def __init__(self, api_key=None, timeframe=TickerResultTimeFrame.Daily, tolerance=0.1):

        if api_key:
            self._api_key = api_key
        else:
            try:
                key = join(dirname(abspath(__file__)), 'key.txt')
                self._api_key = open(key).read().split("\n")[0]
            except Exception as ex:
                raise TickerError('Error reading API key. %s' % str(ex))

        if 0.001 < tolerance < 30:
            self._tolerance = tolerance
        else:
            raise TickerError('Invalid tolerance')

        if isinstance(timeframe, TickerResultTimeFrame):
            self._tf = timeframe
        else:
            raise TickerError('Invalid timeframe')

        self._ts = self._create_internal_endpoint()

    def _create_internal_endpoint(self):

        if not self._api_key:
            raise TickerError('Invalid API key')

        try:
            return TimeSeries(key=self._api_key)
        except ValueError as ve:
            raise TickerError('Internal error on TS creation. %s' % str(ve))

    def get_data(self):

        res = TickerResult()

        data, metadata = None

        try:
            if self._tf == TickerResultTimeFrame.Daily:
                data, metadata = self._ts.get_daily('SPX', outputsize='full')
            if self._tf == TickerResultTimeFrame.Weekly:
                data, metadata = self._ts.get_weekly('SPX', outputsize='full')
            if self._tf == TickerResultTimeFrame.Monthly:
                data, metadata = self._ts.get_monthly('SPX', outputsize='full')
        except Exception as ex:
            raise TickerError('Error getting time series data. %s' % str(ex))

        if not data:
            raise TickerError('Empty time series data result')

        res._tf = self._tf

        return res
