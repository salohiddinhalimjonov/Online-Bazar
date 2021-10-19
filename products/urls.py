from django.urls import path
from .views import ProductListCreateView, ProductDetailView, OrderView, StatisticsView, CategoryView, SliderView, SliderDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('order/', OrderView.as_view(), name='orders'),

    path('orders/statistics', StatisticsView.as_view(), name='order-statistics'),
    path('categories/', CategoryView.as_view()),
    path('slider/', SliderView.as_view()),
    path('slider/<int:pk>/', SliderDetailView.as_view())
]
