from django.shortcuts import render,redirect
from .forms import MarketingPrefernceForm
from .models import MarketingPrefernce
from django.views.generic import UpdateView,View
from django.contrib.messages.views import  SuccessMessageMixin
from django.conf import  settings
from .utils import MailChimp
from django.http import HttpResponse
from .mixins import CsrfExcemptmixin



MAILCHIMP_EMAIL_LIST_ID =getattr(settings,"MAILCHIMP_EMAIL_LIST_ID",None)

class MarketingPrefernceView(SuccessMessageMixin,UpdateView):
    form_class = MarketingPrefernceForm
    template_name = 'marketing/form.html'
    success_url = '/settings/email/'
    success_message = "your preference has been updated"

    def get_object(self, queryset=None):
        user=self.request.user
        obj,created=MarketingPrefernce.objects.get_or_create(user=user)

        return obj
    def get_context_data(self, **kwargs):
        context=super(MarketingPrefernceView, self).get_context_data()
        context['title']="Marketing Preferences"
        return context

    def dispatch(self,request, *args, **kwargs):
        user=self.request.user
        if not user.is_authenticated:
            return redirect('/accounts/login/')
        return super(MarketingPrefernceView, self).dispatch(request,*args, **kwargs)



class MailChimpWebhookView(CsrfExcemptmixin,View):
    # def get(self,request,*args,**kwargs):
    #     return HttpResponse("thank You!")
    def post(self,request,*args,**kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get('data[email]')
            response_status, response = MailChimp().check_subscription_status(email=email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPrefernce.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                        subscribed=is_subbed,
                        mailchimp_subscribed=mailchimp_subbed,
                        mailchimp_msg=str(data)
                    )
        return HttpResponse("thank You!")

# def mailchimp_webhook_view(request):
#     data=request.POST
#     list_id=data.get('data[list_id]')
#     if str(list_id)==str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type=data.get("type")
#         email=data.get('data[email]')
#         response_status,response=MailChimp().check_subscription_status(email=email)
#         sub_status=response['status']
#         is_subbed=None
#         mailchimp_subbed=None
#         if sub_status=="subscribed":
#             is_subbed,mailchimp_subbed=(True,True)
#         elif sub_status=="unsubscribed":
#             is_subbed, mailchimp_subbed = (False, False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs=MarketingPrefernce.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(
#                     subscribed=is_subbed,
#                     mailchimp_subscribed=mailchimp_subbed,
#                     mailchimp_msg=str(data)
#                 )
#     return HttpResponse("thank You!")