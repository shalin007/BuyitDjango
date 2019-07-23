from django.db import models
from billing.models import BillingProfile
import string
# Create your models here.
ADDRESS_TYPES =(
    ('billing','Billing'),
    ('shipping','Shipping'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_type    = models.CharField(max_length=150,choices=ADDRESS_TYPES)
    address         = models.CharField(max_length=150)
    city            = models.CharField(max_length=150)
    state           = models.CharField(max_length=150)
    postal          = models.CharField(max_length=150)



    def __str__(self):
        return '{}'.format(self.billing_profile)
