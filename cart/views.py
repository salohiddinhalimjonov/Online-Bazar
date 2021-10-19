from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from django.utils.translation import ugettext_lazy
from rest_framework.generics import (ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import CartItem
from .serializers import  CartItemSerializer, CartItemUpdateSerializer
class CartItemApiView(ListCreateAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CartItem.objects.filter(user=user)
        return queryset

    def create(self,request, *args, **kwargs):
        user = self.request.user
        product = get_object_or_404(Product, pk=request.data['product'])
        current_item = CartItem.objects.filter(user=user,product=product)
        if user == product.user:
            raise PermissionDenied("This is your product!")

        if current_item.quantity > 0:
            raise NotAcceptable("You already have this item in your shopping cart!")
        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please Enter Your Quantity")

        if quantity > product.quantity:
            raise NotAcceptable("You order quantity more than the seller have")
        cart_item = CartItem(user=user, product=product, quantity=quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        

        return Response(serializer.data, status=status.HTTP_201_CREATED)
class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def retrieve(self,request,*args,**kwargs):
        cart_item = self.get_object()
        if cart_item.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you!")
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self,request,*args,**kwargs):
        cart_item=self.get_object()
        product = get_object_or_404(Product, pk=request.data["product"])

        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")

        try:
            quantity = int(request.data["quantity"])
        except Exception as ex:
            raise ValidationError("Please, input vaild quantity")

        if quantity > product.quantity:
            raise NotAcceptable("Your order quantity more than the seller have")

        serializer = CartItemUpdateSerializer(cart_item)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        cart_item.delete()


        return Response(
            {"detail": ("your item has been deleted.")},
            status=status.HTTP_204_NO_CONTENT,
        )