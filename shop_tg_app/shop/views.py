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
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .services import get_photo_subquery, get_able_sizes, category_sort_params_validation


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
        
        category_sort_params_validation(category_param, sort_param, self.allowed_sorts)
        category_id = int(category_param)
        
        products = Product.objects.filter(category__id=category_id).annotate(
            main_photo=Subquery(get_photo_subquery().values('image')[:1]), 
            main_photo_webp=Subquery(get_photo_subquery().values('image_preview')[:1]),
        ).order_by(sort_param)

        # Базовый layout-контекст
        context.update({
            "show_sort_bar": True,
            "show_home_button": True,  # на странице будет кнопка "на главную"
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
        context = super().get_context_data(**kwargs)
        product = self.product
        
        product_photos = ProductPhoto.objects.filter(product=product).order_by('-priority')
        
        able_sizes = product.sizes.all().order_by('priority')
        # поолучаем наличие на складе размеров
        sizes_availability = get_able_sizes(product, able_sizes=able_sizes)
        
        context.update({
            "sizes_availability": dict(sizes_availability),
            "able_sizes": able_sizes,
            "product": product,
            "product_photos": product_photos,
        })

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

@method_decorator(cache_page(60 * 60), name='dispatch')
class MainPageView(BaseContextMixin, TemplateView):
    template_name = "shop/index.html"
    allowed_sorts = settings.ALLOWED_SORTS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # получаем параметр сортировки
        request = self.request
        sort = request.GET.get("sort")
        if sort not in self.allowed_sorts:
            # сортируем по дефолту по новизне 
            sort = "-created_at"

        # Получаем продукты изначально отсортированые по новизне по дефолку 
        top_products = Product.objects.annotate(
            main_photo=Subquery(
                get_photo_subquery().values('image')[:1]  # Ограничение на выборку только одного фото
            ),
            main_photo_webp=Subquery(
                get_photo_subquery().values('image_preview')[:1]  # Ограничение на выборку только одного фото
        )
        ).order_by(sort)[:settings.MAX_POSTS_ON_MAIN_PAGE if settings.MAX_POSTS_ON_MAIN_PAGE != -1 else None]

        
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
        

        # Фильтрация по поисковому запросу и добавление главного фото
        search_result_products = Product.objects.filter(name__icontains=validated_search_param).annotate(
            main_photo=Subquery(
                get_photo_subquery().values('image')[:1]  # Ограничение на выборку только одного фото
            ),
            main_photo_webp=Subquery(
                get_photo_subquery().values('image_preview')[:1]  # Ограничение на выборку только одного фото
        ))
        
        context.update({
            "products_querry_set": search_result_products,
            "show_sort_bar": True,
        })
        
        
        return context

        
    
    def get(self, request, *args, **kwargs):
        try:
            # получаем параметр поиска из запроса 
            search_param = request.GET.get("search")
            
            
            if not search_param or len(search_param) > settings.MAX_SEARCH_CHARACTERS or len(search_param) < settings.MIN_SEARCH_CHARACTERS:
                return HttpResponseBadRequest("wrong search param")
            # кладем во вьюху валидировнный параметр поиска 
            self.search_param = request.GET.get("search")
            
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))