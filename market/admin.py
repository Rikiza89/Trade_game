from django.contrib import admin
from .models import Stock, Holding, Transaction, PriceHistory
from .utils import update_prices

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'price', 'volatility', 'drift', 'last_update']
    list_filter = ['last_update']
    search_fields = ['symbol', 'name']
    actions = ['update_stock_prices']
    
    def update_stock_prices(self, request, queryset):
        updated = update_prices()
        self.message_user(request, f'Updated prices for {len(updated)} stocks')
    update_stock_prices.short_description = 'Update Prices Now'

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['stock', 'price', 'timestamp']
    list_filter = ['stock', 'timestamp']
    search_fields = ['stock__symbol']
    date_hierarchy = 'timestamp'

@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'shares']
    list_filter = ['stock']
    search_fields = ['user__username', 'stock__symbol']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'transaction_type', 'shares', 'price', 'timestamp']
    list_filter = ['transaction_type', 'timestamp']
    search_fields = ['user__username', 'stock__symbol']
    date_hierarchy = 'timestamp'