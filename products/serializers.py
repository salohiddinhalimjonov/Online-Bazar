from rest_framework import serializers
from .models import Category, Product,  Slider, Order, OurContact
from user.serializers import UserProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


        
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class OrderGetSerializer(serializers.ModelSerializer):
    #region = RegionSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'user',
                  'product', 'quantity', 'status', 'created_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    product = ProductSerializer(many=True)
    #region = RegionSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('user',
                  'product', 'quantity')

