import P
from django.shortcuts import render
from .models import Post, Cart, Product
from .sterializers import Post, CartSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView


class Posts(generics.GenericAPIView):
    permission_classes = permissions.IsAuthenticated,
    authentication_classes = TokenAuthentication,
    def get(self, requests):
        posts = Post.objects.all()
        serializer = P(posts, many=True)
        return Response({
            'data' : serializer.data
        })

class ProductCreate(generics.CreateAPIView):
    serializer_class = P
    queryset = Posts


class CartAddView(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED)

class CartDeleteView(APIView):
    def delete(self, request, product_id):
        user = request.user
        try:
            cart_item = Cart.objects.get(user=user, product_id=product_id)
            cart_item.delete()
            return Response({'message': 'Product removed from cart'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)

class CartListView(APIView):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderListView:
    pass