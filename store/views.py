from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view, action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from .models import Cart, CartItem, Customer, Product, Collection, OrderItem, Review
from .serializers import AddCartItemSerializer, CartSerializer, CartItemSerializer, CustomerSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission


# class ProductList(APIView):
#    def get(self, request):
#     queryset = Product.objects.select_related('collection').all()
#     serializer = ProductSerializer(queryset, many=True, context= { 'request': request })
#     return Response(serializer.data)
  
#    def post(self, request):
#     serializer = ProductSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
    # print(serializer.validated_data)
    # return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetail(APIView):
#   def get(self, request, id):
#     product = get_object_or_404(Product, pk=id)
#     serializer = ProductSerializer(product, context= { 'request': request })
#     return Response(serializer.data)
      
#   def put(self, request, id):
#     product = get_object_or_404(Product, pk=id)
#     serializer = ProductSerializer(product, data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)
     
#   def delete(self, request, id):
#     product = get_object_or_404(Product, pk=id)
#     if product.orderitems.count() > 0:
#       return Response({ 'error': 'Product cannot be deleted because it is associated with an order item.' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     product.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductList(ListCreateAPIView):
#    queryset = Product.objects.all()
#    serializer_class = ProductSerializer
   
#    def get_serializer_context(self):
#       return { 'request': self.request }


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#   queryset = Product.objects.all()
#   serializer_class = ProductSerializer

  # def delete(self, request, pk):
  #   product = get_object_or_404(Product, pk=pk)
  #   if product.orderitems.count() > 0:
  #     return Response({ 'error': 'Product cannot be deleted because it is associated with an order item.' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  #   product.delete()
  #   return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # def get_queryset(self):
    #   queryset = Product.objects.all()
    #   collection_id = self.request.query_params.get('collection_id')
    #   if collection_id is not None:
    #     queryset = queryset.filter(collection_id=collection_id)
    #   return queryset

    def get_serializer_context(self):
      return { 'request': self.request }
    
    def destroy(self, request, *args, **kwargs):
      if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
        return Response({ 'error': 'Product cannot be deleted because it is associated with an order item.' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
      return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
  queryset = Collection.objects.annotate(products_count=Count('products')).all()
  serializer_class = CollectionSerializer
  permission_classes = [IsAdminOrReadOnly]

  def destroy(self, request, *args, **kwargs):
    if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
      return Response({ 'error': 'Collection cannot be deleted because it includes one or more products' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return super().destroy(request, *args, **kwargs)


# class CollectionList(ListCreateAPIView):
#    queryset = Collection.objects.annotate(products_count=Count('products')).all()
#    serializer_class = CollectionSerializer


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk): 
#       collection = get_object_or_404(Collection, pk=pk)
#       if collection.products.count() > 0:
#         return Response({ 'error': 'Collection cannot be deleted because it includes one or more products' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#       collection.delete()
#       return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
  serializer_class = ReviewSerializer

  def get_queryset(self):
    return Review.objects.filter(product_id=self.kwargs['product_pk'])

  def get_serializer_context(self):
    return { 'product_id': self.kwargs['product_pk'] }


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
  queryset = Cart.objects.prefetch_related('items').all()
  serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
  http_method_names = ['get', 'post', 'patch', 'delete']

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return AddCartItemSerializer    
    elif self.request.method == 'PATCH':
      return UpdateCartItemSerializer
    return CartItemSerializer
  
  def get_serializer_context(self):
    return { 'cart_id': self.kwargs['cart_pk'] }
  
  def get_queryset(self):
    return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).all()  


class CustomerViewSet(ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer
  permission_classes = [IsAdminUser]

  # def get_permissions(self):
  #   if self.request.method == 'GET':
  #     return [AllowAny()]
  #   return [IsAuthenticated()]

  @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
  def history(self, request, pk):
    return Response('ok')

  @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
  def me(self, request):
    (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
    if request.method == 'GET':
      serializer = CustomerSerializer(customer)
      return Response(serializer.data)
    elif request.method == 'PUT':
      serializer = CustomerSerializer(customer, request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)
