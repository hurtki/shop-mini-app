from django.shortcuts import render, redirect
from .models import Product, Category
from django.views import View
from django.http import HttpResponseBadRequest


# класс для передачи категорий в шаблон
class LayoutView(View):
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        
        return context
    

# страница которая ест параметры и выдает по ним продукты 
# обязательная категория, сортировка дефолтная по новизне 
class ProductsPageView(LayoutView):
    def get(self, request):
        params = request.get("")
    
    
    
        context = {
            "show_sort_bar": True,
        }
        # сначала мы должны получить параметры запроса если чегото нету то вернуть ошибку
        
        category_param = request.GET.get("category")  # получаем переданный id категории 
        sort_param = request.GET.get("sort") 
        
        if not (category_param and sort_param):
            return HttpResponseBadRequest("no params: category, sort")
        # список доступных сортировок 
        allowed_sorts = ["created_at", 'price', 'price']
        # получаем все категории, у которых нет дочерних
        categories_id_without_children = Category.objects.filter(children__isnull=True).values_list("id", flat=True)
        
        # валидируем 
        if (not category_param.isdigit()) or (sort_param not in allowed_sorts):
            return HttpResponseBadRequest("wrong params")
    
        # преобразуем категорию в айдишник 
        category_id = int(category_param)
        
        if category_id not in categories_id_without_children:
            return HttpResponseBadRequest("bad category given")
        # получили все продукты по категории и отсортировнные 
        products = Product.objects.filter(category__id=category_id).order_by(sort_param)
        
        context["products"] = products
        print(context)

        return render(request, "shop/index.html", context)
        
    
    

# страница с категориями
class InspectPageView(LayoutView):
    def get(self, request, id):
        # здесь у нас будет уже id полученный из url 
    
        # получаем ссылки на фотографии, название продукта 
        # дальше ищем productstock и передаем уже итоговое значение есть или нет для кажого размера 
        
        

        
        
        context = {
            "show_sort_bar": False,
        }
        
        return render(request, template_name="shop/inspect.html", context=context)
    
    



# сюда ничего не будет передаваться, просто продукты отсортировнные по новизне первые 10
# не будет плашки сортировки 
class MainPageView(View):
    pass


# сюда будет в параметрах передаваться строка  что искалась и в шаблон продукта будут возвращаться продукты по поиску 
# плюс будет передаваться сортировка 
# категория передаваться не будет 

class SearchPageView(View):
    pass