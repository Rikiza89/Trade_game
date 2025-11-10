from django.db import models
from accounts.models import User

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_value = models.DecimalField(max_digits=12, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_value']
    
    def __str__(self):
        return f"{self.user.username}: ¥{self.total_value}"