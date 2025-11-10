from django.core.management.base import BaseCommand
from market.utils import update_prices

class Command(BaseCommand):
    help = 'Update stock prices using GBM simulation'
    
    def handle(self, *args, **options):
        updated_stocks = update_prices()
        self.stdout.write(self.style.SUCCESS('Stock prices updated:'))
        for stock in updated_stocks:
            self.stdout.write(f'{stock.symbol}: ¥{stock.price:.2f}')