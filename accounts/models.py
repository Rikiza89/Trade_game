from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=1000000)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=1000000)
    
    def update_total_value(self):
        from market.models import Holding
        holdings_value = sum(
            holding.shares * holding.stock.price 
            for holding in Holding.objects.filter(user=self).select_related('stock')
        )
        self.total_value = self.balance + holdings_value
        self.save()
        
    def __str__(self):
        return self.username