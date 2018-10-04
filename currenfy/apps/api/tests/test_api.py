from rest_framework import status
from rest_framework.test import APITestCase
from api.serializers import BookedTradesSerializer
from booked.models import BookedTrades

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

class ApiTest(APITestCase):

    def test_create_booked_trade(self):
        """
            Allows create a booked trade
        """
        # recording first element of the trade list
        response = self.client.post('/api/booked/', TRADES[0], format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_list_booked_trades(self):
        """
            Test consistency between saved and listed
        """
        saved = []
        # recording remaining elements
        for item in TRADES[1:]:
            response = self.client.post('/api/booked/', item, format='json')
            saved.append(response.data)
            self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        

        for json_trade in saved:
            # queryset first item
            db_trade = BookedTrades.objects.filter(ID=json_trade.get('ID',None))[0]
            # model object 
            obj_trade = BookedTrades(**json_trade)
            # checks if the two dictionaries are equals
            # TO-DO: I'm not sure about its goodness
            self.assertEquals(db_trade, obj_trade)

            
