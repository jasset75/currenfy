from booked.models import BookedTrades
from fixer.converter import Converter
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
from .serializers import BookedTradesSerializer


class BookedTradesSet(viewsets.ModelViewSet):
    """
        API endpoint that interface with Booked Trades
    """
    queryset = BookedTrades.objects.all().order_by('-date_booked')
    serializer_class = BookedTradesSerializer


class SymbolsView(ListAPIView):
    """
        Implements fixer services interface for booking trades
    """
    def get(self, request, format=None):
        """
            Returns list of allowed currency symbols.
        """
        
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

        symbols = Converter.get_symbols()
        content = {
            'symbols': symbols
        }

        return Response(content, status.HTTP_200_OK)


def rate_without_params():
    raise Exception('Not allowed get rate without currency exchange symbols.')

class RateView(ListAPIView):
    """
        Implements fixer services interface for booking trades
    """
    def get(self, request, sell_currency=None, buy_currency=None, format=None):
        """
            Gets exchange rate between `sell_currency` and `buy_currency`.
        """
        
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

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

        return Response(content, status.HTTP_200_OK)
