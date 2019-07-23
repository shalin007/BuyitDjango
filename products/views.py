from django.shortcuts import render
from django.views import generic
from .models import  Product
from django.http import Http404
from django.urls import reverse
from cart.models import Cart
# Create your views here.
class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/product_list.html'
    
    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     print (context)
    #     return context
class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'projectk'

    # def get_context_data(self, **kwargs):
    #     context = super(ProductDetailView, self).get_context_data(**kwargs)
    #     print (context)
    #     return context

class ProductSlugDetailView(generic.DetailView):
    model = Product


    def get_object(self,*args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        try:
            instance=Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404('not found..........')
        except Product.MultipleObjectsReturned:
            qs=Product.objects.filter(slug=slug)
            instance=qs.first()

        return instance
    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'slug':self.slug})

    def get_context_data(self, **kwargs):
         context = super(ProductSlugDetailView, self).get_context_data(**kwargs)
         cart_obj,new_obj=Cart.objects.new_or_get(self.request)
         context['cart']=cart_obj
         return context

