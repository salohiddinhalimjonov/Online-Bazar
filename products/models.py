from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
import os
from user.models import User
from django.conf import settings
from django.utils import timezone



def product_image_path(instance, filename):
    ext = str(filename).split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('thumb/', filename)

def product_video_path(instance, filename):
    ext = str(filename).split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('product/video/', filename)

def slider_path(instance, filename):
    ext = str(filename).split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('product/slider/', filename)


def _expire_at_default():
    return timezone.now() + timezone.timedelta(minutes=settings.CODE_VERIFICATION_EXPIRE_TIME)


class Category(models.Model):

    name = models.CharField(_('Nomi:'), max_length=128)

    class Meta:
        verbose_name = _('Kategoriya')
        verbose_name_plural = _('Kategoriyasi')

    def __str__(self):
        return self.name   


class Product(models.Model):

    UNIT = (('tonna', 'tonna'),
    ('kg', 'kg'),
    ('gramm', 'gramm'),
    ('pachka', 'pachka'),   
    ('dona', 'dona'),)
    DISCOUNT_UNIT = (('%', '%'),
    ('so\'m', 'so\'m'))

    title = models.CharField(_('Nomi:'),max_length=255)
    description = models.TextField(_('Mahsulot haqida batafsil:'), null=True, blank=True)
    cost = models.FloatField(_('Narxi :'))
    image = models.ImageField(_('Rasmi'),upload_to=product_image_path, null=True, blank=True)
    video = models.FileField(_('Videosi:'),upload_to=product_video_path, null=True, blank=True)
    count_in_store = models.IntegerField(_('Zaxiradagi mahsulotlar soni:'),default=0)
    sold_count = models.IntegerField(_('Sotilgan maxsulotlar soni:'),default=0)
    unsold_count = models.IntegerField(_('Sotilmagan mahsulotlar soni:'),default=0)
    onhold_count = models.IntegerField(_('Kutish bo\'limidagilar soni:'),default=0)
    trend = models.BooleanField(_('Modami:'),default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name=_('Kategoriyasi:'),null=True, blank=True)
    unit = models.TextField(_('mahsulot birligi:'),choices=UNIT, default='dona')
    date_created = models.DateTimeField(auto_now_add=True)
    has_discount = models.BooleanField(default=False)
    discount = models.FloatField(_('Chegirma'), default=0)
    discount_unit = models.TextField(_('Chegirma birligi'), choices=DISCOUNT_UNIT, default='%')
    class Meta:
        verbose_name = _('Mahsulot')
        verbose_name_plural = _('Mahsulotlar')

    def __str__(self):
        return self.title    
    
    
        
class Slider(models.Model):
   
    title = models.CharField(max_length=255)
    info = models.TextField()
    image = models.FileField(_('Rasmi:'), upload_to = slider_path,null=True, blank=True)

    class Meta:
        verbose_name = _('Slayd')
        verbose_name_plural = _('Slaydlar')

    def __str__(self):
        return self.title


class Order(models.Model):

    STATUS = (('Pending', 'Pending'),
    ('Yetkazildi', 'Yetkazildi'),
    ('Yetkazilmadi', 'Yetkazilmadi'))
    status = models.TextField(choices=STATUS, default='Pending')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='buyurtmalar')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='buyurtmalar')
    quantity = models.IntegerField(_('Mahsulotlar miqdori:'), default=1)
    total = models.FloatField(_('Mahsulotlarning umumiy summasi'),default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    calculated = models.BooleanField(default=False)
    class Meta:
        verbose_name = _('Buyurtma')
        verbose_name_plural = _('Buyurtmalar')
    

class OurContact(models.Model):
    
    aboutteam = models.TextField(blank=True, null=True)
    app_store = models.CharField(_('App Store'), max_length=255)
    telegram = models.CharField(_('Telegram'), max_length=255)
    facebook = models.CharField(_('Facebook'), max_length=255)
    youtube = models.CharField(_('You Tube'), max_length=255)
    logo = models.FileField(_('Logo'), max_length=255)
    play_market = models.CharField(_('Play Market'), max_length=255)
    phone_number = models.CharField(_('Phone number'), max_length=255)

    