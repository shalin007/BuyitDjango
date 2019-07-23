from django.urls import path,re_path
from . import views


app_name='cart'

urlpatterns=[
    path('',views.cart,name='home'),
    path('update/',views.cart_update,name='update'),
    path('checkout/',views.checkout_home,name='checkout'),
    path('success/',views.success,name='success'),

]