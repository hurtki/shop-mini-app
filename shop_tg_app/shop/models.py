from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from mptt import models as MPTTModels 

class Category(MPTTModels.MPTTModel):
    """
    класс модели категории / реализутся иерархия категорий
    """
    
    name = models.CharField(max_length=20)
    
    # родительская категория, если она есть
    parent = MPTTModels.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    # важность категории, от этого будет зависеть порядок их показа в меню, чем больше тем важннее!
    priority = models.IntegerField(validators=[
        MinValueValidator(-1),
        MaxValueValidator(10000)
    ])
    

    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError("Нельзя создавать категории глубже двух уровней")

class ProductStock(models.Model):
    """
    Модель продукта на складе, связывает продукт, цвет, и размер.
    """

    # сам пррдукт наличие которого на скалде мы описваем 
    product = models.ForeignKey(to="Product", on_delete=models.CASCADE, related_name='stock_items', null=False)
    
    # ссылка на свзяь 
    size = models.ForeignKey(to="Size", on_delete=models.CASCADE, null=False)
    # количество в котором продукт будет на складе
    quantity = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])  

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name}, {self.size.name} — {self.quantity} шт."

    def clean(self):
        # Проверяем, что размер присутствует в списке доступных размеров продукта
        if self.size not in self.product.sizes.all():
            raise ValidationError(f"Размер {self.size.name} не доступен для этого продукта.")
    
    
class Product(models.Model):
    """
    класс модели продукта
    есть вариации и размеры
    тоесть те вариации и размеры которые подключенны через поля они описывают все возможные комбинации продукта
    а уже товары на складе будут описывать что есть а чего нету на данный момент
    """
    
    # категория продукта 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    
    # пока что не оченб понятно как будет сделанно имя но пусть будет 
    name = models.CharField(max_length=50)
    
    description = models.TextField(max_length=500, null=True, blank=True)
    
    # возможные размеры продукта 
    sizes = models.ManyToManyField("Size", related_name="products_with_size", blank=True)
    
    # цена продукта 
    price = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(100000)
    ], default=0)
    
    
    # когда был создан продукт 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class ProductPhoto(models.Model):
    """
    Класс модели фотграфии продукта которую я уже буду привязывать к продукту
    """
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="fotos")
    image = models.ImageField(upload_to="products_photos/")
    
    # порядок в котором будут отображаться фотграфии на странице 
    priority = models.IntegerField(validators=[
        MinValueValidator(-1),
        MaxValueValidator(10000)
    ], default=0)
    
    def __str__(self):
        return f"Фото для {self.product.name} (приоритет {self.priority})"


class Size(models.Model):
    """
    класс модели размера 
    """
    
    name = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return self.name
