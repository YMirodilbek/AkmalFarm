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
]