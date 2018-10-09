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

        response = requests.request("GET", cls._symbols_url)

        # parsing json to dict
        doc = json.loads(response.text)
        if not doc:  # pragma: no cover
            raise Exception('Converter :: Symbols doc is empty.')

        # checks success
        if not doc.get('success',None):  # pragma: no cover
            raise Exception('Converter :: Symbols doc has no symbols.')
        if not doc['success']:
            raise Exception('Converter :: Symbols call not success.')

        # checks symbols key exists
        symbols = doc.get('symbols',None)
        if not symbols:  # pragma: no cover
            raise Exception('Converter :: Symbols doc has no symbols.')

        return sorted(symbols)

    @classmethod
    def get_rate(cls, sell_currency=None, buy_currency=None):
        """
            get rate conversion from sell_currency to buy_currency
        """
        if not sell_currency:  # pragma: no cover
            raise Exception('Converter :: `sell_currency` parameter required.')

        if not buy_currency:  # pragma: no cover
            raise Exception('Converter :: `buy_currency` parameter required.')

        # url endpoint assambly
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
        if base != settings.BASE_CURRENCY:  # pragma: no cover
            raise Exception('Converter :: Base "{}" currency not expected.'.format(base))
        
        # checks if exists rates
        rates = doc.get('rates', None)
        if not rates:  # pragma: no cover
            raise Exception('Converter :: Latest rates doc has no rates.')

        # checks if sell currency has exchange rate
        sell_rate = rates.get(sell_currency, None)
        if not sell_rate:  # pragma: no cover
            raise Exception('Converter :: Sell rate exchange for "{}" currency not found.'.format(sell_currency))

        # checks if buy currency has exchange rate
        buy_rate = rates.get(buy_currency, None)
        if not buy_rate:  # pragma: no cover
            raise Exception('Converter :: Buy rate exchange for "{}" currency not found.'.format(sell_currency))

        # rate calculation
        if sell_currency == settings.BASE_CURRENCY:  # buy_rate is already in the base currency
            exchange_rate = buy_rate
        elif buy_currency == settings.BASE_CURRENCY:  # base currency is the buyer, buy_rate is 1
            exchange_rate = 1/sell_rate
        else:
            # with first multiplier converts to base currency and converts 
            # to final currency with the second
            exchange_rate = buy_rate*(1/sell_rate)  # sell and buy currencies are not the base currency

        # apply rate precision
        return round(exchange_rate, settings.RATE_DECIMAL_PRECISION)
