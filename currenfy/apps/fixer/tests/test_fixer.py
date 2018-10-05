import json
import requests
import datetime
from django.test import TestCase
from django.conf import settings
from fixer.converter import Converter

api_key = settings.FIXER_IO.get('API_KEY', None)


# Fixer endpoints test
class FixerTest(TestCase):

    def test_symbols(self):
        """
            Test to retrieve available currency symbols and descriptions
        """
        # gets existing config urls
        self.assertTrue(api_key)
        symbols_base = settings.FIXER_IO.get('SYMBOLS_URL', None)
        self.assertTrue(symbols_base)
        url = symbols_base.format(api_key)

        # gets symbols data in json format
        response = requests.request("GET", url)

        # parsing json to dict
        doc = json.loads(response.text)
        self.assertTrue(doc)

        # Testing typical values
        self.assertEqual(doc['symbols']['EUR'], 'Euro')
        self.assertEqual(doc['symbols']['GBP'], 'British Pound Sterling')
        self.assertEqual(doc['symbols']['USD'], 'United States Dollar')

    def test_latest(self):
        """
            Test to retrieve latest currency-exchange rates
        """
        # gets existing config urls
        self.assertTrue(api_key)
        latest_base = settings.FIXER_IO.get('LATEST_URL', None)
        self.assertTrue(latest_base)
        url = latest_base.format(api_key)

        # gets symbols data in json format
        response = requests.request("GET", url)

        # parsing json to dict
        doc = json.loads(response.text)
        self.assertTrue(doc)

        # Testing expected values
        self.assertEqual(doc['base'], 'EUR')

        date_ts = datetime.datetime.fromtimestamp(doc['timestamp'])
        self.assertEqual(date_ts.year,datetime.datetime.today().year)

        self.assertTrue(doc['rates']['GBP'])
        self.assertTrue(doc['rates']['USD'])

    def test_get_symbols(self):
        """
            Test converter.Converter.get_symbols()
        """
        symbols = Converter.get_symbols()

        # Testing expected values
        self.assertTrue('EUR' in symbols)
        self.assertTrue('GBP' in symbols)
        self.assertTrue('USD' in symbols)

    def test_conversion_case_1(self):
        """
            Test a fake conversion with retrieved rates
        """
        sell_amount = 1000
        sell_currency = 'GBP'
        buy_currency = 'USD'
        rate = Converter.get_rate(sell_currency=sell_currency, buy_currency=buy_currency)
        buy_amount = sell_amount*rate
        print('{} {} x ({}) {} -> {} {}'.format(sell_amount, sell_currency, 
                                                rate,
                                                buy_currency, 
                                                buy_amount, buy_currency))
        self.assertTrue(buy_amount)

    def test_conversion_case_2(self):
        """
            Test a fake conversion with retrieved rates
        """
        sell_amount = 1000
        sell_currency = 'EUR'
        buy_currency = 'GBP'
        rate = Converter.get_rate(sell_currency=sell_currency, buy_currency=buy_currency)
        buy_amount = sell_amount*rate
        print('{} {} x ({}) {} -> {} {}'.format(sell_amount, sell_currency, 
                                                rate,
                                                buy_currency, 
                                                buy_amount, buy_currency))
        self.assertTrue(buy_amount)

    def test_conversion_case_3(self):
        """
            Test a fake conversion with retrieved rates
        """
        sell_amount = 1000
        sell_currency = 'GBP'
        buy_currency = 'EUR'
        rate = Converter.get_rate(sell_currency=sell_currency, buy_currency=buy_currency)
        buy_amount = sell_amount*rate
        print('{} {} x ({}) {} -> {} {}'.format(sell_amount, sell_currency, 
                                                rate,
                                                buy_currency, 
                                                buy_amount, buy_currency))
        self.assertTrue(buy_amount)
