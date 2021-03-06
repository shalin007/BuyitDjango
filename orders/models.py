from django.db import models
from cart.models import Cart
from django.db.models.signals import  pre_save,post_save,m2m_changed
from ecommerce.utils import unique_order_id_generator
from billing.models import BillingProfile
from address.models import Address
import math
# Create your models here.
ORDER_STATUS_CHOICES=(
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self,billing_profile,cart_obj):
        created=False
        order_qs=Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True,status='created')
        if order_qs.count()==1:
            order_obj=order_qs.first()
        else:
            order_obj=Order.objects.create(billing_profile=billing_profile,cart=cart_obj)
            created=True
        return order_obj,created

class Order(models.Model):
    order_id            = models.CharField(max_length=120,blank=True)
    shipping_address    = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='shipping_address',null=True,blank=True)
    billing_address     = models.ForeignKey(Address,on_delete=models.CASCADE,related_name='billing_address',null=True,blank=True)
    billing_profile     = models.ForeignKey(BillingProfile,on_delete=models.CASCADE,blank=True,null=True)
    cart                = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status              = models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total      = models.DecimalField(default=5.99,max_length=150,decimal_places=2,max_digits=50)
    total               = models.DecimalField(default=5.99,max_length=150,decimal_places=2,max_digits=50)
    active              = models.BooleanField(default=True)


    objects=OrderManager()

    def check_done(self):
        if self.billing_profile and self.shipping_address and self.billing_address and self.total>0:
            return True
        else:
            return False

    def mark_paid(self):
        if self.check_done():
            self.status='paid'
            self.save()
        return self.status


    def __str__(self):
        return self.order_id
    def update_total(self):
         cart_total=self.cart.total
         shipping_total=self.shipping_total
         new_total=math.fsum([cart_total,shipping_total])
         self.total=new_total
         self.save()
         return new_total  
        

def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
    qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

        
pre_save.connect(pre_save_create_order_id,sender=Order)

def post_save_cart_total(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj=instance
        cart_total=cart_obj.total
        cart_id=cart_obj.id
        qs= Order.objects.filter(cart_id=cart_id)
        if qs.count()==1:
            order_obj=qs.first()
            order_obj.update_total()
post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order)