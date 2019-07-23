from django.shortcuts import render
from products.models import Product
from django.views import generic

# Create your views here.

class SearchProducttView(generic.ListView):
    model = Product
    template_name = 'search/view.html'

    def get_context_data(self, **kwargs):
        context = super(SearchProducttView, self).get_context_data(**kwargs)
        context['query']=self.request.GET.get('q')
        return context



    def get_queryset(self):
        request=self.request
        query=request.GET.get('q',None)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.all()