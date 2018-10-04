from booked.models import BookedTrades
from rest_framework import viewsets
from .serializers import BookedTradesSerializer


class BookedTradesSet(viewsets.ModelViewSet):
    """
        API endpoint that interface with Booked Trades
    """
    queryset = BookedTrades.objects.all().order_by('-date_booked')
    serializer_class = BookedTradesSerializer
