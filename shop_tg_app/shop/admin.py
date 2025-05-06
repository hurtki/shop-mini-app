from django.contrib import admin
from .models import Product, Size, ProductStock, Category, ProductPhoto
from django.utils.html import mark_safe

# инлайн показ продуктов на складе связанных с моделью конкретного продукта 
class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1  # количество пустых строк для добавления новых элементов по умолчанию

class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1  # Количество пустых строк для добавления новых фотографий по умолчанию
    fields = ('image', 'priority', 'image_preview')  # Указываем, какие поля будут отображаться
    readonly_fields = ['image_preview']  # Если не хочется, чтобы заказчик мог редактировать путь к изображению
    
    # метод описывающий столбик превью фото в админке, возвразащает html строку
    def image_preview(self, obj) -> str:
        if obj.image:
            print(obj.image.url)
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "Нет изображения"
    image_preview.short_description = "Превью"
    
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')  # что показывать в списке
    search_fields = ('name', 'id')  # поля для поиска
    list_filter = ('category',)  # фильтрация по категориям
    inlines = [ProductStockInline, ProductPhotoInline]  # связь с ProductStock и ProductPhoto через инлайн
    
    def get_search_results(self, request, queryset, search_term):
        # Сначала обычный поиск
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Потом — если ввели чистое число, ищем по ID
        if search_term.isdigit():
            queryset |= self.model.objects.filter(id=int(search_term))

        return queryset, use_distinct
    

# редактирование категори
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'parent')  # что показывать в списке категорий
    search_fields = ('id', )
    list_filter = ('parent',)

# размер на админке
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    search_fields = ('name',)

# весь склад продуктов, чтобы можно было смотреть все продукты на складе 
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity')
    list_filter = ('product__category', 'product', 'size')
    search_fields = ('product__name',)
    ordering = ('product__name',)
    
    list_editable = ['quantity'] # что можно редактировать в списке 
    
    # описываем что нельзя менять ничего в detailview
    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return True

# Регистрация моделей
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ProductStock, ProductStockAdmin)


