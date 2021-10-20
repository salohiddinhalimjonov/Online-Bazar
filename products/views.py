from django.shortcuts import render
from .paginations import DefaultLimitOffsetPagination
from django.db.models import Q, Sum
from django.http import Http404

from .serializers import (CategorySerializer, ProductSerializer,SliderSerializer, OrderGetSerializer,
                        OrderCreateSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import generics, status
from rest_framework.response import Response       
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from user.models import User
from .permissions import IsAdminOrReadOnly
from datetime import date, timedelta
from .models import Product,  Order, Category, Slider

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultLimitOffsetPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]# QUESTION 1 --- why only create?
        return [perm() for perm in permission_classes]

    def get(self, request, *args, **kwargs):
        category_id = request.query_params.get('category')
        search = request.query_params.get('search')
        queryset = Product.objects.all()
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if search:
            searching_list = str(search).split('')
            queries = [Q(name__icontains=word) for word in searching_list]
            query = queries.pop()
            for item in queries:
                query |= item

            queryset = Product.objects.filter(query)
        paginator = DefaultLimitOffsetPagination()
        return paginator.generate_response(queryset, ProductSerializer, request)        
    
       

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    #The task of this class is to help customers to retrieve(get the product that you want from list of products),
    #to update(adding or decreasing the amount of product.),
    #to delete(deleting the product that you don't need to buy from you basket)
    queryset = Product.objects.all()# QUESTION 2  ----   Are the sentences written below correct?
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class OrderView(APIView):
    def get_permissions(self):
        if self.request.method=='POST' or self.request.method=='GET':
            permission_classes = [IsAuthenticated,]
        return [perm() for perm in permission_classes]    
        
    def post(self, request, *args, **kwargs):
        data = request.data.copy() # QUESTION 3 ---- request.data.copy() - what does it return?
        total = data.get('total', None)#QUESTION 4 ----- if I change total's amount, does it also change in the web page?
        product = data.get('product', None)
        quantity = product.get('quantity', None)
        
        # if product['discount'] == 0 :
        #     total = quantity * product['cost']
        #     data.update({'total': total})
        # elif product['discount'] > 0 and product['status']=='%':
        #     total = quantity * (product['cost'] - product['discount'] * product['cost']/100)  
        #     data.update({'total': total})
            
        # elif product['discount'] > 0 and product['status'] == 'so\'m':
        #     total = quantity * (product['cost'] - product['discount'])
        #     data.update({'total': total})
            

        serializer = OrderCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Buyurtma yaratildi'}, serializer.data, status=status.HTTP_201_CREATED)

    

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        if request.user.is_superuser:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(user=request.user)

        
            
        if search:
            searching_list = str(search).split(' ')
            queries = [Q(user_full_name__icontains=word) |
                       Q(user_full_name__icontains=word) |
                       Q(status__icontains=word) |
                       Q(product__title__icontains=word) for word in searching_list]
            query = queries.pop()
            for itemss in queries:
                query |= itemss

            queryset = queryset.filter(query)

        paginator = DefaultLimitOffsetPagination()
        return paginator.generate_response(queryset, OrderGetSerializer, request)
        
class OrderPatchView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self,request, pk, *args, **kwargs):
        
        try:
            order = Order.objects.get(id=pk)
        except:
            raise ValidationError('Object was not found!')    

        command = request.data.get('status')
        product = order.product
        if command == 'Pending':
            order.status = 'Pending'
            order.save(update_fields=['status'])
            if not order.calculated:
            
                product.count_in_store -= order.quantity#Bu zaxiradagi mahsulotlarni sotib olinayotgan mahsulotlardan ayiradi
                # Bu orqali agar keyingi mijozlarni chalkashishlikdan saqlaydi. Misol uchun: zaxiradagi mahsulotlar 1 dona qolsa va 
                #u Hold bo'lgan bo'lsa, bu albatta databasadagi count_in_storeda ham o'zgarishi kerak.
                product.onhold_count += order.quantity
                product.save(update_fields=['count_in_store','onhold_count'])
        if command == 'Yetkazildi':
            order.status = 'Yetkazildi'
            order.save(update_fields=['status'])
            if not order.calculated:
                
                product.sold_count += order.quantity
                product.onhold_count -= order.quantity
                product.save(update_fields=['sold_count', 'onhold_count'])
                order.calculated = True
                order.save(update_fields=['calculated'])
            return Response({'message': 'status changed to Yetkazildi'})

        if command == 'Yetkazilmadi':
            order.status = 'Yetkazilmadi'
            order.save(update_fields=['status'])
            
            if not order.calculated:
                product.count_in_store += order.quantity 
                product.unsold_count += order.quantity
                #product.sold_count -= order.quantity  -- if status changed to yetkazilmadi after status was yetkazildi
                product.onhold_count -= order.quantity
                product.save(update_fields=['count_in_store', 'unsold_count', 'onhold_count'])
                order.calculated = True
                order.save(update_fields=['calculated'])   
            elif order.calculated:
                product.count_in_store += order.quantity
                product.unsold_count += order.quantity
                product.sold_count -= order.quantity
                product.onhold_count -= order.quantity
                product.save(update_fields=['count_in_store', 'unsold_count', 'sold_count', 'onhold_count'])
                
            return Response({'message': 'status changed to Yetkazilmadi'})
        return Response({'message': 'provide with command=Yetkazildi, Yetkazilmadi'})
class StatisticsView(APIView):
    permission_classes = [IsAdminUser,]
    def get(self, request, *args, **kwargs ):

        chosen_day = request.query_params.get('day')
        day_filter = request.query_params.get('date')
        order_count_filter = request.query_params.get('orders')
        sold_filter = request.query_params.get('sold')
        unsold_filter = request.query_params.get('unsold')
        onhold_filter = request.query_params.get('onhold')
        income_filter = request.query_params.get('income')
        orders = Order.objects.all()
        
        if chosen_day:
            day_result = {}
            day_result['day'] = chosen_day
            day_result['order_count'] = orders.filter(created_at=chosen_day).count()
            day_result['sold'] = orders.filter(created_at=chosen_day, status='Yetkazildi').count()
            day_result['unsold'] = orders.filter(created_at=chosen_day, status='Yetkazilmadi').count()
            day_result['onhold'] = orders.filter(created_at=chosen_day, status='Pending').count()
            orders = orders.filter(created_at=chosen_day, status='Yetkazildi')
            total = 0
            for x in orders:
                total += x.total
            day_result['total_income'] = total
            return Response([day_result])
        else:
            today = date.today()
            date_list = [today - timedelta(days=day)
                         for day in range(10)]
            result = []

            for chosen_day in date_list:
                day_result = {}
                day_result['day'] = chosen_day
                day_result['order_count'] = orders.filter(created_at=chosen_day).count()
                day_result['sold'] = orders.filter(created_at=chosen_day, status='Yetkazildi').count()
                day_result['unsold'] = orders.filter(created_at=chosen_day, status='Yetkazilmadi').count()
                day_result['hold'] = orders.filter(created_at=chosen_day, status='Pending').count()
                orders = orders.filter(created_at=chosen_day, status='Yetkazildi')
                total = 0
                if orders:
                    
                    for x in orders:
                      total += x.total
                    day_result['total_income'] = total
                else:
                    day_result['total_income'] = total    
                result.append(day_result)

                
            if day_filter == 'true':
                result = sorted(result, key=lambda i: i['day'], reverse=False)

            if order_count_filter == 'true':
                result = sorted(
                    result, key=lambda i: i['order_count'], reverse=True)
            if sold_filter == 'true':
                result = sorted(result, key=lambda i: i['sold'], reverse=True)
            if unsold_filter == 'true':
                result = sorted(
                    result, key=lambda i: i['unsold'], reverse=True)

            if income_filter == 'true':
                result = sorted(
                    result, key=lambda i: i['income'], reverse=True)

            if onhold_filter == 'true':
                result = sorted(
                    result, key=lambda i: i['onhold'], reverse=True)
            return Response(result)



       


class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ('list', 'GET'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [perm() for perm in permission_classes]

    def get(self, request):
        qs = Category.objects.all()
        paginator = DefaultLimitOffsetPagination
        return paginator.generate_response(qs, CategorySerializer, request)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'category was created'}, status=status.HTTP_201_CREATED)


class SliderView(generics.ListCreateAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = (IsAdminOrReadOnly,)


class SliderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = (IsAdminOrReadOnly,)
