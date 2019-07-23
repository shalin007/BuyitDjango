from django import  forms
from .models import MarketingPrefernce



class MarketingPrefernceForm(forms.ModelForm):
    subscribed= forms.BooleanField(label=' Recieve Marketing Email?',required=False)
    class Meta:
        model=MarketingPrefernce
        fields=['subscribed']