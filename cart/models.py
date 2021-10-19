from django.db import models
from products.models import Product
from django.conf import settings


class CartItem(models.Model):#An Abstract Base Class model that provides self-managed created and modified fields.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
