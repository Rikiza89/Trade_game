import random
import math
from .models import Stock, PriceHistory

def update_prices():
    """Update all stock prices using Geometric Brownian Motion"""
    updated_stocks = []
    for stock in Stock.objects.all():
        drift = stock.drift
        vol = stock.volatility
        epsilon = random.gauss(0, 1)
        change = math.exp((drift - (vol**2)/2) + vol*epsilon)
        stock.price = max(float(stock.price) * change, 1)
        stock.save()
        
        # Save price history
        PriceHistory.objects.create(stock=stock, price=stock.price)
        
        updated_stocks.append(stock)
    return updated_stocks