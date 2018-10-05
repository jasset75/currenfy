from django.test import TestCase
from booked.models import BookedTrades
from booked.models import ID_HEADER, ID_LENGTH


# Basic CRU tests
class CruTest(TestCase):

    def check_id(self, id):
        # checks if exists
        self.assertTrue(id)
        # checks if alphanumeric
        self.assertTrue(id.isalnum())
        # checks has the correct header
        self.assertEqual(id[:len(ID_HEADER)], ID_HEADER)
        # checks has the exact length
        self.assertEqual(len(id), len(ID_HEADER)+ID_LENGTH)

    def test_insert_booked_trade(self):
        """
            Inserts new record
        """
        btr = BookedTrades(
            sell_currency='GBP',
            sell_amount=1000,
            buy_currency='USD',
            rate=1.2561
        )
        btr.save()
        # checks ID is ok
        self.check_id(btr.ID)
        # checks if trade have been correctly calculated
        self.assertEqual(btr.buy_amount, btr.sell_amount*btr.rate)

    def test_update_booked_trade(self):
        """
            Update record
        """
        # insert new record
        btr = BookedTrades(
            sell_currency='GBP',
            sell_amount=900,
            buy_currency='EUR',
            rate=1.14
        )
        btr.save()
        
        # checks __str__ is ID
        self.assertEqual(str(btr), btr.ID)
        # checks if trade have been correctly calculated
        self.assertEqual(btr.buy_amount, btr.sell_amount*btr.rate)
        # update
        btr.sell_amount = 1100
        btr.save()
        # checks if trade have been correctly calculated
        self.assertEqual(btr.buy_amount, btr.sell_amount*btr.rate)
