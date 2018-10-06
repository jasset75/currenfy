from booked.models import BookedTrades
from django.conf import settings
from rest_framework import serializers


class BookedTradesSerializer(serializers.Serializer):
    
    ID = serializers.CharField(read_only=True, max_length=len(settings.ID_HEADER) + settings.ID_LENGTH)
    sell_currency = serializers.CharField(max_length=3, required=True)
    sell_amount = serializers.DecimalField(max_digits=settings.MAX_AMOUNT_LEN, decimal_places=2, required=True)
    buy_currency = serializers.CharField(max_length=3, required=True)
    buy_amount = serializers.DecimalField(read_only=True, max_digits=settings.MAX_AMOUNT_LEN, decimal_places=2)
    rate = serializers.DecimalField(max_digits=9, decimal_places=4, required=True)
    date_booked = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `BookedTrades` instance, given the validated data.
        """
        return BookedTrades.objects.create(**validated_data)
