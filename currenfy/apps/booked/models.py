import string, random
from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import pre_save

ID_HEADER = 'TR'
ID_LENGTH = 7
MAX_AMOUNT_LEN = 11


# identifier generator to identify Booked Trades
def g_identifier():
    """
        Generates an unique identifier based on random ID_LENGTH length word
    """
    return ID_HEADER + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(ID_LENGTH))
    

# Booked Trades of foreign exchange
class BookedTrades(models.Model):

    ID = models.CharField(primary_key=True, max_length=len(ID_HEADER)+ID_LENGTH, verbose_name='Trade Id.')
    sell_currency = models.CharField(max_length=3, verbose_name='Sell CCY')
    sell_amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=2, verbose_name='Sell Amount')
    buy_currency = models.CharField(max_length=3, verbose_name='Buy CCY')
    buy_amount = models.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=2, verbose_name='Buy Amount')
    rate = models.DecimalField(max_digits=9, decimal_places=4, verbose_name='Rate')
    date_booked = models.DateTimeField(auto_now_add=True, verbose_name='Date Booked')

    class Meta:
        verbose_name = 'Booked Trade'
        verbose_name_plural = 'Booked Trades'
        ordering = ['-date_booked']

    def __str__(self):
        return '{}'.format(self.ID)
        
# This mechanism allow generate unique IDs for each currency trading exchange
@receiver(pre_save, sender=BookedTrades)
def booked_trades_pre_save_handler(sender, instance, *args, **kwargs):

    if instance._state.adding:
        collision = True
        # tries until generate an unused ID
        while collision:
            id_candidate = g_identifier()
            with transaction.atomic():
                try:
                    collision = (
                        sender.objects
                            .select_for_update()
                            .get(ID=id_candidate)
                    )
                except BookedTrades.DoesNotExist: # ID exists
                    collision = False
                if not collision:
                    instance.ID = id_candidate
    # consistency asurance    
    instance.buy_amount = instance.sell_amount * instance.rate
