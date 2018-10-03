from django.contrib import admin
from .models import BookedTrades

# Booked Trades Admin
@admin.register(BookedTrades)
class BookedTradesAdmin(admin.ModelAdmin):
    readonly_fields = ['ID', 'buy_amount']
    list_display = ['ID', 'sell_currency', 'sell_amount', 'buy_currency', 'buy_amount', 'rate', 'date_booked']
    ordering = ['-date_booked']
    search_fields = ['ID', 'sell_currency', 'sell_amount', 'buy_currency', 'buy_amount', 'rate', 'date_booked']
    date_hierarchy = 'date_booked'
