from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.http import  is_safe_url
from .models import BillingProfile,Card

# Create your views here.


import stripe
stripe.api_key='sk_test_D2zxuBv5yQdAe6mttiVuKvqe00TZN4kQOx'
STRIPE_PUB_KEY='pk_test_CBHbYFSpZMRQjqocFlW4WBpy00rGt4LLm1'

def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")

    nextUrl=None
    next_=request.GET.get('next')
    if is_safe_url(next_,request.get_host()):
        nextUrl=next_
    return render(request,'billing/payment.html',{'publish_key':STRIPE_PUB_KEY,"nextUrl":nextUrl})


@ensure_csrf_cookie
def payment_method_createview(request):
    if request.method=='POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"error":"can't find this user"})
        token=request.POST.get("token")
        if token is not None:
            # card_response = stripe.Customer.create_source(billing_profile.customer_id,source=token)
            # new_card_obj=Card.objects.add_new(billing_profile,card_response)
            new_card_obj = Card.objects.add_new(billing_profile, token)

        return JsonResponse({'message':'Success! your card is added'})
    return HttpResponse("error")