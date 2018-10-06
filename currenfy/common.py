from django.test import TestCase
from django.conf import settings


# Base TestCase
class CurrenfyTest(TestCase):

    def check_id(self, id):
        """
            checks booked trade ID is well-formed
        """
        # checks if exists
        self.assertTrue(id)
        # checks if alphanumeric
        self.assertTrue(id.isalnum())
        # checks has the correct header
        self.assertEqual(id[:len(settings.ID_HEADER)], settings.ID_HEADER)
        # checks has the exact length
        self.assertEqual(len(id), len(settings.ID_HEADER) + settings.ID_LENGTH)

    def check_rate(self, rate):
        """
            checks rate is a correct float number with correct precision
        """
        self.assertTrue(rate)
        self.assertEqual(rate, round(rate, settings.RATE_DECIMAL_PRECISION))

    def check_amount(self, amount):
        """
            checks amount is a correct float number with correct precision
        """
        self.assertTrue(amount)
        self.assertEqual(amount, round(amount, settings.AMOUNT_DECIMAL_PRECISION))
