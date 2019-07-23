from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save,pre_save
from accounts.models import GuestEmail
User=get_user_model()
from django.urls import reverse
import stripe
stripe.api_key='sk_test_D2zxuBv5yQdAe6mttiVuKvqe00TZN4kQOx'
STRIPE_PUB_KEY='pk_test_CBHbYFSpZMRQjqocFlW4WBpy00rGt4LLm1'

# Create your models here.

class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user=request.user
        guest_email_id = request.session.get('guest_email_id')
        billing_profile_created=False
        billing_profile=None
        if user.is_authenticated:
            # logged in user  remember payment
            billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)

        elif guest_email_id is not None:
            # guest dont remember
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(
                                                                email=guest_email_obj.email)
        else:
            pass
        return billing_profile,billing_profile_created




class BillingProfile(models.Model):
    # id          = models.PositiveIntegerField(primary_key=True)
    user        = models.OneToOneField(User,blank=True,null=True, on_delete=models.CASCADE)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now=True)
    time_stamp  = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120,null=True,blank=True)

    objects=BillingProfileManager()

    def __str__(self):
        return self.email
    
    def charge(self,order_obj,card=None):
        return Charge.objects.do(self,order_obj,card)
    
    def get_cards(self):
        return self.card_set.all()

    @property
    def has_card(self):
        card_qs=self.get_cards()
        return card_qs.exists()

    @property
    def default_card(self):
        default_cards=self.get_cards().filter(active=True,default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def get_payment_method_url(self):
        return reverse('billing-payment')
    
    def set_cards_inactive(self):
        card_qs=self.get_cards()
        card_qs.update(active=False)
        return card_qs.filter(active=True).count()

def user_created_reciever(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_created_reciever,sender=User)

def billing_profile_created_reciever(sender,instance,*args,**kwargs):
    if not instance.customer_id and instance.email:
        '''requesting to stripe API call'''
        customer=stripe.Customer.create(
            email=instance.email
        )
        
        instance.customer_id=customer.id
pre_save.connect(billing_profile_created_reciever,sender=BillingProfile)


class CardManager(models.Manager):
    def all(self,*args,**kwargs):
        return self.get_queryset().filter(active=True)
    
    def add_new(self,billing_profile,token):
        if token:
            stripe_response = stripe.Customer.create_source(billing_profile.customer_id, source=token)
            new_card=self.model(
                billing_profile =   billing_profile,
                stripe_id       =   stripe_response.id,
                brand           =   stripe_response.brand,
                country         =   stripe_response.country,
                exp_month       =   stripe_response.exp_month,
                exp_year        =   stripe_response.exp_year,
                last4           =   stripe_response.last4
            )
            new_card.save()
            return new_card
        return None

class Card(models.Model):
    billing_profile =   models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_id       =   models.CharField(max_length=120)
    brand           =   models.CharField(max_length=120,null=True,blank=True)
    country         =   models.CharField(max_length=120,null=True,blank=True)
    exp_month       =   models.IntegerField(null=True,blank=True)
    exp_year        =   models.IntegerField(null=True,blank=True)
    last4           =   models.CharField(max_length=120,null=True,blank=True)
    default         =   models.BooleanField(default=True)
    active          =   models.BooleanField(default=True)
    timestamp       =   models.DateTimeField(auto_now_add=True)
    
    objects= CardManager()
    
    
    def __str__(self):
        return "{} {}".format(self.brand,self.last4)
    


def new_card_post_save_reciever(sender,instance,created,*args,**kwargs):
    if instance.default:
        billing_profile=instance.billing_profile
        qs=Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)
post_save.connect(new_card_post_save_reciever,sender=Card)
class ChargeManager(models.Manager):
    def do(self,billing_profile,order_obj,card=None):
        card_obj=card
        if card_obj is None:
            cards=billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj=cards.first()
        if card_obj is None:
            return False,"NO CARDS AVAILABLE"
        
        c = stripe.Charge.create(
            amount=int(order_obj.total*100),
            currency="usd",
            customer= billing_profile.customer_id,
            source=card_obj.stripe_id , # obtained with Stripe.js
            metadata={'order_id':order_obj.order_id}
        )
        
        new_charge_obj=self.model(
            billing_profile=billing_profile,
            stripe_id=c.stripe_id,
            paid=c.paid,
            refunded=c.refunded,
            outcome=c.outcome,
            outcome_type=c.outcome['type'],
            seller_message=c.outcome.get('seller_message'),
            risk_level=c.outcome.get('risk_level')
        )
        new_charge_obj.save()
        return new_charge_obj.paid,new_charge_obj.seller_message
    
    
class Charge(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id           = models.CharField(max_length=120)
    paid                = models.BooleanField(default=False)
    refunded            = models.BooleanField(default=False)
    outcome             = models.TextField(null=True,blank=True)
    outcome_type        = models.CharField(max_length=120,null=True,blank=True)
    seller_message      = models.CharField(max_length=120,null=True,blank=True)
    risk_level          = models.CharField(max_length=120,null=True,blank=True)
    
    
    objects=ChargeManager()