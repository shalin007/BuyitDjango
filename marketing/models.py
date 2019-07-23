from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from .utils import MailChimp

# Create your models here.
class MarketingPrefernce(models.Model):
    user                 = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subscribed           = models.BooleanField(default=True)
    mailchimp_subscribed = models.NullBooleanField(blank=True)
    mailchimp_msg        = models.TextField(null=True,blank=True)
    timestamp            = models.DateTimeField(auto_now_add=True)
    update               = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email


def marketing_pref_create_reciever(sender,instance,created,*args,**kwargs):
    if created:
        status_code,response_data=MailChimp().add_email(instance.user.email)
        

post_save.connect(marketing_pref_create_reciever,sender=MarketingPrefernce)

def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            # subscribing user
            status_code, response_data = MailChimp().subscribe(instance.user.email)
        else:
            # unsubscribing user
            status_code, response_data = MailChimp().unsubscribe(instance.user.email)

        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data

pre_save.connect(marketing_pref_update_receiver, sender=MarketingPrefernce)

# def marketing_pref_update_reciever(sender,instance,*args,**kwargs):
#     if instance.subscribed != instance.mailchimp_subscribed:
#         if instance.subscribed:
#             #subscribing user
#             status_code,response_data =  MailChimp().subscribe(instance.user.email)
#         else:
#             #unsubscibing user
#             status_code,response_data = MailChimp().unsubscribe(instance.user.email)
#
#         if response_data['status']=='subscribed':
#             instance.subscribed=True
#             instance.mailchimp_subscribed=True
#             instance.mailchimp_msg=response_data
#         else:
#             instance.subscribed = False
#             instance.mailchimp_subscribed = False
#
# pre_save.connect(marketing_pref_update_reciever, sender=MarketingPrefernce)



def make_marketing_pref_reciever(sender,instance,created,*args,**kwargs):
    '''' USER MODEL '''
    if created:
        MarketingPrefernce.objects.get_or_create(user=instance)

post_save.connect(make_marketing_pref_reciever,sender=settings.AUTH_USER_MODEL)

