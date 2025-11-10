from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('transactions/', views.TransactionsView.as_view(), name='transactions'),
    path('api/prices/', views.ApiPricesView.as_view(), name='api_prices'),
    path('api/market-prices/', views.ApiMarketPricesView.as_view(), name='api_market_prices'),
    path('api/price-history/<int:stock_id>/', views.ApiPriceHistoryView.as_view(), name='api_price_history'),
]