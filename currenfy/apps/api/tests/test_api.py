from django.urls import reverse
from rest_framework import status
# from rest_framework.test import APITestCase
from currenfy.common import CurrenfyTest
from api.serializers import BookedTradesSerializer
from booked.models import BookedTrades
from django.conf import settings

TRADES = [
    {
        "sell_currency": "EUR",
        "sell_amount": "1000.00",
        "buy_currency": "GBP",
        "rate": "0.8900",
    },        
    {
        "sell_currency": "GBP",
        "sell_amount": "900.00",
        "buy_currency": "EUR",
        "buy_amount": "1057.50",
        "rate": "1.1750",
    },
    {
        "sell_currency": "GBP",
        "sell_amount": "900.00",
        "buy_currency": "EUR",
        "buy_amount": "1057.50",
        "rate": "1.1750",
    },
    {
        "sell_currency": "EUR",
        "sell_amount": "1100.00",
        "buy_currency": "USD",
        "buy_amount": "1381.71",
        "rate": "1.2561",
    }
]

class ApiTest(CurrenfyTest):

    def item_check(self, item):
        """
            checks booked trade is correct
        """
        self.assertTrue(item.get('ID', None))
        self.assertTrue(item.get('sell_amount', None))
        self.assertTrue(item.get('sell_currency', None))
        self.assertTrue(item.get('buy_amount', None))
        self.assertTrue(item.get('buy_currency', None))
        self.assertTrue(item.get('rate', None))
        self.assertTrue(item.get('date_booked', None))
        rate = float(item.get('rate', None))
        sell_amount = float(item.get('sell_amount', None))
        buy_amount = float(item.get('buy_amount', None))
        self.check_rate(rate)
        self.check_amount(sell_amount)
        self.check_amount(buy_amount)
        self.assertEqual(buy_amount, sell_amount*rate)

    def create_booked_trades(self):
        res = []
        # recording remaining elements
        for item in TRADES[1:]:
            response = self.client.post(reverse('booked-list'), data=item, format='json')
            res.append(response.data)
            self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        return res

    def test_create_booked_trades_endpoint(self):
        """
            Test create booked trades: consistency between saved and recorded
        """
        # create booked trades for testing
        saved = self.create_booked_trades()
        # iterates over saved items and verifies that are properly recorded in DB
        for json_trade in saved:
            # queryset first item
            db_trade = BookedTrades.objects.filter(ID=json_trade.get('ID',None))[0]
            # model object 
            obj_trade = BookedTrades(**json_trade)
            # checks if the two dictionaries are equals
            # TO-DO: I'm not sure about its goodness
            self.assertEquals(db_trade, obj_trade)

    def test_list_booked_trades_endpoint(self):
        """
            Test listing booked trades
        """
        # create booked trades for testing
        saved = self.create_booked_trades()
        # retrieving booked trades
        response = self.client.get(reverse('booked-list'), format='json')
        booked_trades = response.data
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # iterates over listed items and verifies integrity 
        for btr in booked_trades:
            self.item_check(btr)

    def test_fixer_symbols_endpoint(self):
        """
            Test API symbols endpoint
        """
        # calling the fixer API's symbols endpoint
        response = self.client.get(reverse('fixer-symbols'), format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # `symbols` key returns a list of symbols
        symbols = response.data.get('symbols', None)
        self.assertTrue(symbols)

        # testing expected values
        self.assertTrue('EUR' in symbols)
        self.assertTrue('GBP' in symbols)
        self.assertTrue('USD' in symbols)

    def test_fixer_rate_endpoint(self):
        """
            Test a fake conversion with retrieved rates
        """
        sell_currency = 'GBP'
        buy_currency = 'USD'

        # calling the fixer API's rate endpoint
        rate_url = reverse('fixer-rate', args=[sell_currency, buy_currency])
        response = self.client.get(rate_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # checks expected fields
        res_rate = response.data.get('rate', None)
        res_sell_currency = response.data.get('sell_currency', None)
        res_buy_currency = response.data.get('buy_currency',None)    

        # checks rate is correct
        self.check_rate(float(response.data.get('rate', None)))

        # checks consistency of currencies 
        self.assertEqual(sell_currency, res_sell_currency)
        self.assertEqual(buy_currency, res_buy_currency)

        print('{} > {} > {}'.format(res_sell_currency, res_rate, res_buy_currency))
