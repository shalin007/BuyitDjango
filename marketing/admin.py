from django.contrib import admin
from .models import  MarketingPrefernce
# Register your models here.

class MarketingPrefernceAdmin(admin.ModelAdmin):
    list_display = ['__str__','subscribed','update']
    readonly_fields = ['mailchimp_msg', 'timestamp', 'update']
    class Meta:
        model= MarketingPrefernce
        fields=['user','subscribed','mailchimp_msg','mailchimp_subscribed','timestamp','update']
admin.site.register(MarketingPrefernce,MarketingPrefernceAdmin)