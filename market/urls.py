from django.urls import path
from . import views

urlpatterns = [
    path('', views.MarketView.as_view(), name='market'),
    path('buy/<int:stock_id>/', views.BuyStockView.as_view(), name='buy_stock'),
    path('sell/<int:stock_id>/', views.SellStockView.as_view(), name='sell_stock'),
]