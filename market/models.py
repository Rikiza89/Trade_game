from django.db import models
from accounts.models import User

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volatility = models.FloatField(default=0.02)
    drift = models.FloatField(default=0.0005)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.symbol} - {self.name}"

class PriceHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['stock', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.stock.symbol} - ¥{self.price} at {self.timestamp}"

class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='holdings')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'stock']
    
    def __str__(self):
        return f"{self.user.username} - {self.stock.symbol}: {self.shares}"

class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    TRANSACTION_TYPES = [
        (BUY, 'BUY'),
        (SELL, 'SELL'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.shares} {self.stock.symbol}"