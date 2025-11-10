from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from decimal import Decimal
from .models import Stock, Holding, Transaction

class MarketView(LoginRequiredMixin, View):
    def get(self, request):
        stocks = Stock.objects.all()
        holdings_dict = {h.stock_id: h.shares for h in request.user.holdings.all()}
        return render(request, 'market.html', {'stocks': stocks, 'holdings': holdings_dict})

class BuyStockView(LoginRequiredMixin, View):
    def post(self, request, stock_id):
        stock = get_object_or_404(Stock, id=stock_id)
        try:
            shares = int(request.POST.get('shares', 0))
            if shares <= 0:
                raise ValueError("Invalid share amount")
        except ValueError:
            messages.error(request, 'Invalid number of shares')
            return redirect('market')
        
        total_cost = stock.price * shares
        
        if request.user.balance < total_cost:
            messages.error(request, 'Insufficient balance')
            return redirect('market')
        
        request.user.balance -= total_cost
        request.user.save()
        
        holding, created = Holding.objects.get_or_create(
            user=request.user,
            stock=stock,
            defaults={'shares': 0}
        )
        holding.shares += shares
        holding.save()
        
        Transaction.objects.create(
            user=request.user,
            stock=stock,
            transaction_type=Transaction.BUY,
            shares=shares,
            price=stock.price
        )
        
        request.user.update_total_value()
        
        messages.success(request, f'Successfully bought {shares} shares of {stock.symbol}')
        return redirect('market')

class SellStockView(LoginRequiredMixin, View):
    def post(self, request, stock_id):
        stock = get_object_or_404(Stock, id=stock_id)
        try:
            shares = int(request.POST.get('shares', 0))
            if shares <= 0:
                raise ValueError("Invalid share amount")
        except ValueError:
            messages.error(request, 'Invalid number of shares')
            return redirect('market')
        
        try:
            holding = Holding.objects.get(user=request.user, stock=stock)
        except Holding.DoesNotExist:
            messages.error(request, 'You do not own this stock')
            return redirect('market')
        
        if holding.shares < shares:
            messages.error(request, 'Insufficient shares')
            return redirect('market')
        
        total_revenue = stock.price * shares
        
        request.user.balance += total_revenue
        request.user.save()
        
        holding.shares -= shares
        if holding.shares == 0:
            holding.delete()
        else:
            holding.save()
        
        Transaction.objects.create(
            user=request.user,
            stock=stock,
            transaction_type=Transaction.SELL,
            shares=shares,
            price=stock.price
        )
        
        request.user.update_total_value()
        
        messages.success(request, f'Successfully sold {shares} shares of {stock.symbol}')
        return redirect('market')