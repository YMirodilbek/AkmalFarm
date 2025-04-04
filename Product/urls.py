from _pyrepl.commands import delete

from django.urls import path
from .views import *
urlpatterns = [
    path('',Index),
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path('cart/',cart_view, name="cart"),
    path("increase-quantity/<int:item_id>/", increase_quantity, name="increase_quantity"),
    path("decrease-quantity/<int:item_id>/", decrease_quantity, name="decrease_quantity"),
    path('remove_from_cart/<int:product_id>/', DeleteProduct, name="delete"),
    path('search/', search_products, name='search_products'),
    path('productdetail/<int:pk>/' , ProductDetailView.as_view(), name='product_detail'),
    path('checkout/',checkout_view, name='checkout'),
    path('myaccount/',Myaccount),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('toggle/<int:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('contact/',Contact),
    # path("checkout/", checkout, name="checkout"),
]