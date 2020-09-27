from django.urls import path 
from . import views


app_name="App_Order"

urlpatterns = [
    path('cart/',views.cart_view,name="cart"),
    path('add/<pk>/',views.add_to_cart,name="add"),
    path('remove/<pk>/',views.remove_form_cart,name="remove")
]
