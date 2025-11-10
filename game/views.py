from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from market.models import Transaction, Stock, PriceHistory
from market.utils import update_prices
from .models import Leaderboard

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user.update_total_value()
        holdings = user.holdings.select_related('stock').all()
        recent_transactions = user.transactions.select_related('stock')[:10]
        
        context = {
            'user': user,
            'holdings': holdings,
            'recent_transactions': recent_transactions,
        }
        return render(request, 'dashboard.html', context)

class LeaderboardView(LoginRequiredMixin, View):
    def get(self, request):
        for user in User.objects.all():
            user.update_total_value()
            Leaderboard.objects.update_or_create(
                user=user,
                defaults={'total_value': user.total_value}
            )
        
        top_users = Leaderboard.objects.select_related('user')[:10]
        context = {'top_users': top_users}
        return render(request, 'leaderboard.html', context)

class TransactionsView(LoginRequiredMixin, View):
    def get(self, request):
        transactions = request.user.transactions.select_related('stock').all()
        context = {'transactions': transactions}
        return render(request, 'transactions.html', context)

class ApiPricesView(LoginRequiredMixin, View):
    def get(self, request):
        # Update all stock prices
        update_prices()
        
        # Get user's updated holdings
        user = request.user
        user.refresh_from_db()
        user.update_total_value()
        
        holdings = []
        for holding in user.holdings.select_related('stock').all():
            holdings.append({
                'stock_id': holding.stock.id,
                'symbol': holding.stock.symbol,
                'shares': holding.shares,
                'price': float(holding.stock.price),
                'value': float(holding.shares * holding.stock.price)
            })
        
        return JsonResponse({
            'balance': float(user.balance),
            'total_value': float(user.total_value),
            'holdings': holdings
        })

class ApiMarketPricesView(LoginRequiredMixin, View):
    def get(self, request):
        # Update all stock prices
        update_prices()
        
        stocks = []
        for stock in Stock.objects.all():
            stocks.append({
                'id': stock.id,
                'symbol': stock.symbol,
                'price': float(stock.price)
            })
        
        return JsonResponse({'stocks': stocks})

class ApiPriceHistoryView(LoginRequiredMixin, View):
    def get(self, request, stock_id):
        timeframe = request.GET.get('timeframe', '1h')
        
        # Calculate time delta based on timeframe
        now = timezone.now()
        time_deltas = {
            '5m': timedelta(minutes=5),
            '15m': timedelta(minutes=15),
            '1h': timedelta(hours=1),
            '6h': timedelta(hours=6),
            '1d': timedelta(days=1),
            '1w': timedelta(weeks=1),
            '1M': timedelta(days=30),
            '3M': timedelta(days=90),
            '1y': timedelta(days=365),
            'all': timedelta(days=3650)  # 10 years
        }
        
        delta = time_deltas.get(timeframe, timedelta(hours=1))
        since = now - delta
        
        history = PriceHistory.objects.filter(
            stock_id=stock_id,
            timestamp__gte=since
        ).values('price', 'timestamp')
        
        data = {
            'labels': [h['timestamp'].strftime('%Y-%m-%d %H:%M:%S') for h in history],
            'prices': [float(h['price']) for h in history]
        }
        
        return JsonResponse(data)