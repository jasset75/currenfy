from rest_framework import status
from rest_framework.test import APITestCase


class ApiTest(APITestCase):
    def test_create_booked_trade(self):
        """
            Allows create a booked trade
        """
        data = {
            "sell_currency": "EUR",
            "sell_amount": "1000.00",
            "buy_currency": "GBP",
            "rate": "0.8900",
        }
        response = self.client.post('/api/booked/', data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
