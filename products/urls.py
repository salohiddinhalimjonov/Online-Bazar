from django.urls import path
from .views import ProductListCreateView, ProductDetailView, OrderView, StatisticsView, CategoryView, SliderView,OrderPatchView, SliderDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('order/', OrderView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderPatchView.as_view()),
    path('order/statistics/', StatisticsView.as_view(), name='order-statistics'),
    path('categories/', CategoryView.as_view()),
    path('slider/', SliderView.as_view()),
    path('slider/<int:pk>/', SliderDetailView.as_view())
]
