from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.BillingProfile)

admin.site.register(models.Card)
admin.site.register(models.Charge)