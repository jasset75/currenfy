from booked.models import BookedTrades
from rest_framework import serializers


class BookedTradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookedTrades
        fields = ['sell_currency', 'sell_amount', 'buy_currency', 'rate', 'date_booked']