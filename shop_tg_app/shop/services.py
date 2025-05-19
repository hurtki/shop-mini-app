# вынесенная бизнес-логика вьюшек
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




def get_photo_subquery():
    """получение фотографий продукта, отсортированных по приоритету"""
    return ProductPhoto.objects.filter(product=OuterRef('pk')).order_by('-priority')

def get_able_sizes(product, able_sizes):
    """получение доступных размеров продукта"""
    
    # Для каждого размера проверяем наличие на складе
    sizes_availability = {}
    # перебираем все размеры продукта
    for size in able_sizes:
        # Проверяем, есть ли этот размер на складе с количеством > 0
        stock = ProductStock.objects.filter(product=product, size=size).first()  # Получаем первый объект на складе для этого размера
        sizes_availability[size.id] = stock is not None and stock.quantity > 0  # Если stock есть и количество больше 0, то True
    return sizes_availability

def category_sort_params_validation(category_param, sort_param, allowed_sorts):
    """валидация параметров сортировки и категории"""
    
    if not (category_param and sort_param):
        raise ValueError("no params: category, sort")
        
    if (not category_param.isdigit()) or (sort_param not in allowed_sorts):
        raise ValueError("wrong params")
    
    category_id = int(category_param)
    
    # Проверяем, что категория не является родительской
    categories_id_without_children = Category.objects.filter(
        children__isnull=True
    ).values_list("id", flat=True)
    
    if category_id not in categories_id_without_children:
        raise ValueError("bad category given")