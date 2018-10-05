import json
import requests
from django.conf import settings


class Converter():
    """
        This class encapsulate Fixer communications
    """
    # fixer endpoints
    _api_key = settings.FIXER_IO.get('API_KEY', None)
    _symbols_base = settings.FIXER_IO.get('SYMBOLS_URL', None)
    _symbols_url = _symbols_base.format(_api_key)
    _latest_base_symbols = settings.FIXER_IO.get('LATEST_URL_SYMBOLS', None)

    @classmethod
    def get_symbols(cls):
        """
            Returns a list with available currency symbols
        """

        # gets symbols data in json format
        response = requests.request("GET", cls._symbols_url)

        # parsing json to dict
        doc = json.loads(response.text)
        if not doc:  # pragma: no cover
            raise Exception('Converter :: Symbols doc is empty.')

        symbols = doc.get('symbols',None)
        if not symbols:  # pragma: no cover
            raise Exception('Converter :: Symbols doc has no symbols.')

        return doc['symbols'].keys()

    @classmethod
    def get_rate(cls, sell_currency='EUR', buy_currency='GBP'):
        """
            get rate conversion from sell_currency to buy_currency
        """
        latest_url = cls._latest_base_symbols.format(cls._api_key,
                                                     ', '.join([sell_currency, buy_currency]))
        # gets EUR exchange rates in json format
        response = requests.request("GET", latest_url)

        # parsing json to dict
        doc = json.loads(response.text)
        if not doc:  # pragma: no cover
            raise Exception('Converter :: Latest rates doc is empty.')

        # checks if base currency is the expected
        base = doc.get('base', None)
        if base != 'EUR':  # pragma: no cover
            raise Exception('Converter :: Base "{}" currency not expected.'.format(base))
        
        # checks if exists rates
        rates = doc.get('rates', None)
        if not rates:  # pragma: no cover
            raise Exception('Converter :: Latest rates doc has no rates.')

        # checks if sell currency has exchange rate
        sell_rate = rates.get(sell_currency,None)
        if not sell_rate:  # pragma: no cover
            raise Exception('Converter :: Sell rate exchange for "{}" currency not found.'.format(sell_currency))

        # checks if buy currency has exchange rate
        buy_rate = rates.get(buy_currency,None)
        if not buy_rate:  # pragma: no cover
            raise Exception('Converter :: Buy rate exchange for "{}" currency not found.'.format(sell_currency))

        if sell_currency == 'EUR':  # buy_rate is already in the base currency
            return buy_rate
        elif buy_currency == 'EUR':  # base currency is the buyer, buy_rate is 1
            return 1/sell_rate
        else:
            return sell_rate*buy_rate # sell and buy currencies are not the base currency


