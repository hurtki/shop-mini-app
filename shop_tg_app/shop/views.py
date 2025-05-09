from django.shortcuts import render, redirect
from .models import Product, Category, ProductPhoto
from django.views import View
from django.http import HttpResponseBadRequest
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Concat
from django.db.models import ImageField
from django.conf import settings
from django.views.generic import TemplateView
from .mixins import BaseContextMixin


# страница которая ест параметры и выдает по ним продукты 
# обязательная категория, сортировка дефолтная по новизне 
class ProductsPageView(BaseContextMixin, TemplateView):
    template_name = "shop/index.html"
    allowed_sorts = ["created_at", 'price']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        request = self.request
        category_param = request.GET.get("category")
        sort_param = request.GET.get("sort")
        
        if not (category_param and sort_param):
            raise ValueError("no params: category, sort")
        
        if (not category_param.isdigit()) or (sort_param not in self.allowed_sorts):
            raise ValueError("wrong params")
        
        category_id = int(category_param)
        categories_id_without_children = Category.objects.filter(
            children__isnull=True
        ).values_list("id", flat=True)
        
        if category_id not in categories_id_without_children:
            raise ValueError("bad category given")
        
        photo_subquery = ProductPhoto.objects.filter(
            product=OuterRef('pk')
        ).order_by('-priority').values('image')[:1]
        
        products = Product.objects.filter(category__id=category_id).annotate(
            main_photo=Subquery(photo_subquery)
        ).order_by(sort_param)

        # Базовый layout-контекст
        context.update({
            "show_sort_bar": True,
            "products_querry_set": products
        })
        
        return context

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
    
    

# страница с категориями
class InspectPageView(BaseContextMixin, TemplateView):
    template_name = "shop/inspect.html"
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

        
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
    
    



# сюда ничего не будет передаваться, просто продукты отсортировнные по новизне первые 10
# не будет плашки сортировки 
class MainPageView(BaseContextMixin, TemplateView):
    template_name = "shop/index.html"
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

        
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))


# сюда будет в параметрах передаваться строка  что искалась и в шаблон продукта будут возвращаться продукты по поиску 
# плюс будет передаваться сортировка 
# категория передаваться не будет 

class SearchPageView(BaseContextMixin, TemplateView):
    template_name = "shop/index.html"
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

        
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))