from django.db import models

from . import Basket
from .product import Post


class Order(models.Model):
    user = models.ForeignKey(to='api_auth.CustomUser', on_delete=models.CASCADE)
    basket = models.ManyToManyField(Basket)
    quantity = models.IntegerField(default=1)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post}"

    def save(self, *args, **kwargs):
        self.price = sum([card.price for card in self.basket])

