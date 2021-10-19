from django.urls import path
from .views import CartItemApiView, CartItemView
urlpatterns = [
    path("cart_item/", CartItemApiView.as_view()),
    path("cart_item/<int:pk>/", CartItemView.as_view()),
]