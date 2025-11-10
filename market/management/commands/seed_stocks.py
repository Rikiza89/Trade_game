from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from market.models import Stock, PriceHistory
import random
import math

class Command(BaseCommand):
    help = 'Generate historical price data for existing stocks'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days of history to generate'
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=5,
            help='Interval in minutes between price points'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        interval = options['interval']
        
        stocks = Stock.objects.all()
        if not stocks:
            self.stdout.write(self.style.ERROR('No stocks found. Run seed_stocks first.'))
            return
        
        now = timezone.now()
        total_points = (days * 24 * 60) // interval
        
        for stock in stocks:
            self.stdout.write(f'Generating history for {stock.symbol}...')
            
            current_price = float(stock.price)
            timestamp = now - timedelta(days=days)
            
            for i in range(total_points):
                # Use GBM to generate realistic price movement
                drift = stock.drift
                vol = stock.volatility
                epsilon = random.gauss(0, 1)
                change = math.exp((drift - (vol**2)/2) + vol*epsilon)
                current_price = max(current_price * change, 1)
                
                PriceHistory.objects.create(
                    stock=stock,
                    price=current_price,
                    timestamp=timestamp
                )
                
                timestamp += timedelta(minutes=interval)
            
            self.stdout.write(self.style.SUCCESS(
                f'Created {total_points} price points for {stock.symbol}'
            ))