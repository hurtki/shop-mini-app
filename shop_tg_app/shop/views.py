from django.shortcuts import render

# главная страница сайта 
def main_page(request):
    return render(request, template_name="shop/index.html")

# страница с категориями
def inspect_page(request):
    return render(request, template_name="shop/inspect.html")

