from django.shortcuts import render, redirect
from .models import Product, Category, ProductPhoto, ProductStock
from django.views import View
from django.http import HttpResponseBadRequest
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Concat
from django.db.models import ImageField
from django.conf import settings
from django.views.generic import TemplateView
from .mixins import BaseContextMixin
from django.shortcuts import get_object_or_404


# страница которая ест параметры и выдает по ним продукты 
# обязательная категория, сортировка дефолтная по новизне 
class ProductsPageView(BaseContextMixin, TemplateView):
    template_name = "shop/index.html"
    allowed_sorts = settings.ALLOWED_SORTS

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
            "products_querry_set": products # только вот здесь идет запрос к объектам 
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
        context = super().get_context_data(**kwargs)
        product = self.product
        
        product_photos = ProductPhoto.objects.filter(product=product).order_by('-priority')
        able_sizes = product.sizes.all()
        # Для каждого размера проверяем наличие на складе
        sizes_availability = {}
        for size in able_sizes:
            # Проверяем, есть ли этот размер на складе с количеством > 0
            stock = ProductStock.objects.filter(product=product, size=size).first()  # Получаем первый объект на складе для этого размера
            sizes_availability[size.id] = stock is not None and stock.quantity > 0  # Если stock есть и количество больше 0, то True
        
        
        context["sizes_availability"] = dict(sizes_availability) 
        context["able_sizes"] = able_sizes
        context["product"] = product
        context["product_photos"] = product_photos
        return context

        
    
    def get(self, request, *args, **kwargs):
        try:
            product_id = self.kwargs.get("id")
            self.product = get_object_or_404(Product, id=product_id)       
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
    
    



# сюда ничего не будет передаваться, просто продукты отсортировнные по новизне первые 10
# не будет плашки сортировки 
class MainPageView(BaseContextMixin, TemplateView):
    template_name = "shop/index.html"
    allowed_sorts = settings.ALLOWED_SORTS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request
        sort = request.GET.get("sort")
        if sort not in self.allowed_sorts:
            sort = "-created_at"
        
       # Получаем главное фото через подзапрос
        photo_subquery = ProductPhoto.objects.filter(
            product=OuterRef('pk')
        ).order_by('-priority')  # Сортируем по приоритету, не ограничивая результат срезом

        # Получаем 10 самых новых продуктов с аннотированным главным фото
        top_products = Product.objects.annotate(
            main_photo=Subquery(
                photo_subquery.values('image')[:1]  # Ограничение на выборку только одного фото
            )
        ).order_by(sort)[:10]
        
        context.update({
            "products_querry_set": top_products,
            "show_sort_bar": True,
            
        })

        return context

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
        context = super().get_context_data(**kwargs)
        # получаем валидированный параметр 
        validated_search_param = self.search_param
        
        # Получаем подзапрос для главного фото
        photo_subquery = ProductPhoto.objects.filter(
            product=OuterRef('pk')
        ).order_by('-priority')  # Сортируем по приоритету, чтобы выбрать самое главное фото

        # Фильтрация по поисковому запросу и добавление главного фото
        search_result_products = Product.objects.filter(name__icontains=validated_search_param).annotate(
            main_photo=Subquery(
                photo_subquery.values('image')[:1]  
            )
        )
        
        
        context.update({
            "products_querry_set": search_result_products,
            "show_sort_bar": True,
        })
        
        
        return context

        
    
    def get(self, request, *args, **kwargs):
        try:
            # получаем параметр поиска из запроса 
            search_param = request.GET.get("search")
            
            Product.objects.filter(name__icontains=search_param)
            
            if not search_param or len(search_param) > settings.MAX_SEARCH_CHARACTERS or len(search_param) < settings.MIN_SEARCH_CHARACTERS:
                return HttpResponseBadRequest("wrong search param")
            # кладем во вьюху валидировнный параметр поиска 
            self.search_param = request.GET.get("search")
            
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))