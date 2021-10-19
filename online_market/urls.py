from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('products/', include('products.urls')),
    path('user/', include('user.urls'))
]

