from django.shortcuts import render

class PlaceOrderView(APIView):
    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
            )
        cart_items.delete()
        return Response({'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)

class OrderListView(APIView):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderAcceptView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'accepted'
            order.save()
            return Response({'message': 'Order accepted'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
