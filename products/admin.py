from django.contrib import admin

from .models import Category, Product, Slider, Order, OurContact

admin.site.register([Category, Product, Slider, Order, OurContact])