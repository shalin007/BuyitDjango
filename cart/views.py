from django.shortcuts import render,redirect
from orders.models  import Order
from . import models
from products.models import Product
from accounts.forms import LoginForm,GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from address.forms import AddressForm

from address.models import Address

# Create your views here.c

# def cart_create(user=None):
#      cart_object = models.Cart.objects.create(user=None)
#      print('cart created')
#      return  cart_object

def cart(request):
     cart_obj,new_obj=models.Cart.objects.new_or_get(request)
     # cart_id=request.session.get('cart_id',None)
     # # if cart_id is None:
     # #      cart_obj = models.Cart.objects.create(user=None)
     # #      request.session['cart_id']=cart_obj.id
     # #      print ('new cart created')
     # qs= models.Cart.objects.filter(id=cart_id)
     # print (qs)
     # if qs.count()==1:
     #      print('exists')
     #      cart_obj=qs.first()
     #      if request.user.is_authenticated and cart_obj.user is None:
     #           cart_obj.user=request.user
     #           cart_obj.save()
     # else:
     #      cart_obj=models.Cart.objects.new(user=request.user)
     #      request.session['cart_id']=cart_obj.id
     return render(request,'cart/view.html',{'cart':cart_obj})

def cart_update(request):
     product_id=request.POST.get('product_id')
     product_obj=Product.objects.get(id=product_id)
     cart_obj, new_obj = models.Cart.objects.new_or_get(request)
     if product_obj in cart_obj.products.all():
          cart_obj.products.remove(product_obj)
     else:
          cart_obj.products.add(product_obj)
     request.session['cart_count']=cart_obj.products.count()
     return render(request,'cart/view.html',{'cart':cart_obj})

def checkout_home(request):
     cart_obj, new_obj = models.Cart.objects.new_or_get(request)
     order_obj=None
     if new_obj or cart_obj.products.count()==0:
          return redirect('cart:home')
     # user=request.user
     # billing_profile=None
     login_form=LoginForm()
     guest_form=GuestForm()
     address_form=AddressForm()
     billing_address_form=AddressForm()
     billing_address_id=request.session.get('billing_address_id')
     shipping_address_id=request.session.get('shipping_address_id')


     # guest_email_id=request.session.get('guest_email_id')
     # if user.is_authenticated:
     #      #logged in user  remember payment
     #      billing_profile,billing_profile_created= BillingProfile.objects.get_or_create(user=user,email=user.email)
     #
     # elif guest_email_id is not None:
     #      #guest dont remember
     #      guest_email_obj=GuestEmail.objects.get(id=guest_email_id)
     #      billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
     # else:
     #      pass
     billing_profile, billing_guest_profile_created = BillingProfile.objects.new_or_get(request)
     has_card=None
     if billing_profile is not None:
          order_obj,order_obj_created= Order.objects.new_or_get(billing_profile,cart_obj)

          if shipping_address_id:
               order_obj.shipping_address=Address.objects.get(id=shipping_address_id)
               del request.session['shipping_address_id']
          if billing_address_id:
               order_obj.billing_address = Address.objects.get(id=billing_address_id)
               del request.session['billing_address_id']
          if billing_address_id or shipping_address_id:
               order_obj.save()
          has_card=billing_profile.has_card

          if request.method=='POST':
               'check whether order is done'
               is_prepared=order_obj.check_done()
               if is_prepared:
                    did_charge,chrg_msg=billing_profile.charge(order_obj)
                    if did_charge:
                         order_obj.mark_paid()
                         request.session['cart_count']=0
                         del request.session['cart_id']
                         if not billing_profile.user:
                              billing_profile.set_cards_inactive()
                         return redirect('cart:success')

                    else:
                         return redirect('cart:success')
          # if order_qs.count() == 1 and order_qs is not None:
          #     order_obj=order_qs.first
          # else:
          #      # old_order_qs = Order.objects.filter(cart=cart_obj,active=True).exclude(billing_profile=billing_profile)
          #      # print(old_order_qs)
          #      # if old_order_qs.exists():
          #      #      old_order_qs.update(active=False)
          #      order_obj = Order.objects.create(billing_profile=billing_profile,cart=cart_obj)
          # moved to model manager


     context={
          'object': order_obj,
          'billing_profile':billing_profile,
          'login_form':login_form,
          'guest_form':guest_form,
          'address_form':address_form,
          'billing_address_form':billing_address_form,
          "has_card":has_card
     }
     return  render(request,'cart/checkout.html',context)

def success(request):
     return render(request,'cart/success.html',{})