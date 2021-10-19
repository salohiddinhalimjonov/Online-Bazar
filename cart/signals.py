from products.models import Order
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import CartItem

@receiver(post_save, sender=CartItem)
def create_order(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        quantity = instance.quantity
        product = instance.product
        total = quantity * product.cost
        if product.discount > 0 and product.discount_unit=='%' and total:
           total = quantity * (product.cost - product.discount * product.cost/100)  
        elif product.discount > 0 and product.discount_unit == 'so\'m' and total:
            total = quantity * (product.cost - product.discount)
        Order.objects.create(user=user, quantity=quantity, product=product, total=total)
        print('Order created!')

@receiver(post_save, sender=CartItem)
def save_order(sender, instance,created, **kwargs):
    if not created:
        user = instance.user
        obj = Order.objects.get(user=user)
        obj.quantity = instance.quantity
        obj.product = instance.product
        obj.total = obj.quantity * obj.product.cost
        if obj.product.discount > 0 and obj.product.discount_unit=='%' and obj.total:
               obj.total = obj.quantity * (obj.product.cost - obj.product.discount * obj.product.cost/100)  
        elif obj.product.discount > 0 and obj.product.discount_unit == 'so\'m' and obj.total:
            obj.total = obj.quantity * (obj.product.cost - obj.product.discount)
        obj.save()
        print('Order updated!')


@receiver(pre_delete, sender=CartItem)
def delete_order(sender, instance, **kwargs):
    user = instance.user
    obj = Order.objects.get(user=user)
    obj.delete()
    print('Order deleted!')