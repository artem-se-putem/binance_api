from django.db import models
from django.contrib.auth.models import User


class Crypto(models.Model):
    symbol = models.CharField(max_length=10, unique=True, default='hey')
    name = models.CharField(max_length=50, default='hey')
    price = models.DecimalField(max_digits=20, decimal_places=10, default='100')
    volume = models.DecimalField(max_digits=20, decimal_places=10, default='100')
    change_24h = models.DecimalField(max_digits=20, decimal_places=10, default='100')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.symbol} ---- {self.price}'


class Favorite_crypto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'crypto',)
    
    def __str__(self):
        return f'{self.user} ---- {self.crypto}'


