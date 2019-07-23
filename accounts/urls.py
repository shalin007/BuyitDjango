
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
# from products.views import ProductDetailView
# app_name='accounts'

urlpatterns = [

    path('login/',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('register/guest/', views.guest_register_view, name='guest_register'),


]