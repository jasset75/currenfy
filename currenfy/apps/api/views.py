from booked.models import BookedTrades
from fixer.converter import Converter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
from .serializers import BookedTradesSerializer


class BookedTradesSet(viewsets.ModelViewSet):
    """
        API endpoint that interface with Booked Trades
    """
    queryset = BookedTrades.objects.all().order_by('-date_booked')
    serializer_class = BookedTradesSerializer


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
def get_rate(sell_currency, buy_currency):
    if not sell_currency:
        content = {'error': 'Sell currency must be specified.'}
        return Response(content, status.HTTP_400_BAD_REQUEST)
    if not buy_currency:
        content = {'error': 'Buy currency must be specified.'}
        return Response(content, status.HTTP_400_BAD_REQUEST)
    rate = Converter.get_rate(sell_currency=sell_currency, buy_currency=buy_currency)
    content = {
        'sell_currency': sell_currency,
        'buy_currency': buy_currency,
        'rate': rate
    }
    return Response(content, status.HTTP_400_BAD_REQUEST)
