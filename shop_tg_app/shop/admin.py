from django.contrib import admin
from .models import Product, Color, Size, ProductStock, Category

class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1  # количество пустых строк для добавления новых элементов по умолчанию

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')  # что показывать в списке
    search_fields = ('name',)  # поля для поиска
    list_filter = ('category',)  # фильтрация по категориям
    inlines = [ProductStockInline]  # связь с ProductStock (цвет и размер) через инлайн

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'parent')  # что показывать в списке категорий
    search_fields = ('name',)
    list_filter = ('parent',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)  # цвет на админке
    search_fields = ('name',)

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # размер на админке
    search_fields = ('name',)

# Регистрация моделей
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
