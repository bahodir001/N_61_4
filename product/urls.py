from django.urls import path

from .views import (
    Posts, ProductCreate, CartAddView, CartDeleteView, CartListView,
    PlaceOrderView, OrderListView, OrderAcceptView,
    LikeToggleView
                           )

urlpatterns = [
    path('', Posts.as_view()),
    path('create', ProductCreate.as_view())
    path('cart/add/', CartAddView.as_view()),
    path('cart/delete/<int:product_id>/', CartDeleteView.as_view()),
    path('cart/', CartListView.as_view()),

    path('order/', PlaceOrderView.as_view()),
    path('order/list/', OrderListView.as_view()),
    path('order/accept/<int:order_id>/', OrderAcceptView.as_view()),

    path('like/<int:product_id>/', LikeToggleView.as_view()),
]