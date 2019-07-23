from django.urls import path,re_path
from .views import ProductListView,ProductDetailView,ProductSlugDetailView


urlpatterns=[
    path('',ProductListView.as_view(),name='product_list'),
    # re_path(r'^products/(?P<pk>\d+)/$',ProductDetailView.as_view(),name='product_detail'),
    re_path(r'^products/(?P<slug>[\w-]+)/$',ProductSlugDetailView.as_view(), name='product_detail'),
]