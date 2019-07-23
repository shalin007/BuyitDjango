from django.urls import path,re_path
from .views import SearchProducttView

app_name='search'

urlpatterns=[
    path('',SearchProducttView.as_view(),name='query'),

]