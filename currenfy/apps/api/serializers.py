from booked.models import BookedTrades
from booked.models import MAX_AMOUNT_LEN, ID_HEADER, ID_LENGTH
from rest_framework import serializers


class BookedTradesSerializer(serializers.Serializer):
    ID = serializers.CharField(read_only=True, max_length=len(ID_HEADER)+ID_LENGTH)
    sell_currency = serializers.CharField(max_length=3, required=True)
    sell_amount = serializers.DecimalField(max_digits=MAX_AMOUNT_LEN, decimal_places=2, required=True)
    buy_currency = serializers.CharField(max_length=3, required=True)
    buy_amount = serializers.DecimalField(read_only=True, max_digits=MAX_AMOUNT_LEN, decimal_places=2)
    rate = serializers.DecimalField(max_digits=9, decimal_places=4, required=True)
    date_booked = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `BookedTrades` instance, given the validated data.
        """
        return BookedTrades.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `BookedTrades` instance, given the validated data.
        """
        instance.sell_currency = validated_data.get('sell_currency', instance.sell_currency)
        instance.sell_amount = validated_data.get('sell_amount', instance.sell_amount)
        instance.buy_currency = validated_data.get('buy_currency', instance.buy_currency)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance
