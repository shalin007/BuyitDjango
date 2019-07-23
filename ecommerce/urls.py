"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
# from products.views import ProductDetailView
from django.conf import settings
from django.conf.urls.static import static
from address.views import checkout_address_create_view
from billing.views import payment_method_view,payment_method_createview
from marketing.views import MarketingPrefernceView,MailChimpWebhookView
urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',views.Home,name='home'),
    path('checkout/address/create/',checkout_address_create_view,name='checkout_address_create_view'),
    path('accounts/',include('accounts.urls')),
    path('product/',include('products.urls')),
    path('billing/checkout/',payment_method_view,name='billing-payment'),
    path('billing/checkout/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('search/',include('search.urls',namespace='search')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('settings/email/',MarketingPrefernceView.as_view(),name='marketing_pref'),
    path('webhooks/mailchimp/', MailChimpWebhookView.as_view(), name='webhooks-mailchimp')

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



