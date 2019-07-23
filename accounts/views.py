from django.urls import path
from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm,GuestForm
from django.contrib.auth import login,authenticate,get_user_model,logout
from django.utils.http import is_safe_url
from django.views.generic import CreateView,FormView
User=get_user_model()
from django.urls import reverse
from .models import GuestEmail
# from django.views.generic import L

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    netx_post = request.POST.get('next')
    redirect_path = next_ or netx_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email =GuestEmail.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
            # context['form'] = Login_form()
        else:
                return redirect('/register/')

    return redirect('/register/')



class LoginView(FormView):
    form_class = LoginForm
    success_url = '/products/product_list'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        

        request = self.request
        next_ = request.GET.get('next')
        netx_post = request.POST.get('next')
        redirect_path = next_ or netx_post or None

        user = authenticate(request, username=email, password=password)
        if user is not None:
            
            login(request, user)
            
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            # context['form'] = Login_form()
            else:
                return redirect('/product')
        return  super(LoginView, self).form_invalid(form)


# def login_page(request):
#     form=LoginForm(request.POST or None)
#     context = {
#         'form': form
#     }
#     next_=request.GET.get('next')
#     netx_post=request.POST.get('next')
#     redirect_path=next_ or netx_post or None
#     if form.is_valid():
#
#         username=form.cleaned_data.get('username')
#         password=form.cleaned_data.get('password')
#         user=authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path,request.get_host()):
#                 return redirect(redirect_path)
#             # context['form'] = Login_form()
#             else:
#                 return redirect('/product')
#         else:
#                 print('not authenticated')
#     return render(request,'accounts/login.html',context)






class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login/'

# def register_page(request):
#     form=RegisterForm(request.POST or None)
#     context={
#         'form':form
#     }
#     if form.is_valid():
#         form.save()
#
#         # username = form.cleaned_data.get('username')
#         # password = form.cleaned_data.get('password')
#         # email = form.cleaned_data.get('email')
#         # user=User.objects.create_user(username,email,password)
#         # return redirect('home')
#
#
#     return render(request,'accounts/register.html',context)

def logout_view(request):
    logout(request)
    return redirect('/product')

