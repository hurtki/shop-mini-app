from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """класс модели категории / реализутся иерархия категорий"""
    
    name = models.CharField(max_length=20)
    
    # родительская категория, если она есть
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    # важность категории, от этого будет зависеть порядок их показа в меню, чем больше тем важннее!
    
    priority = models.IntegerField(validators=[
        MinValueValidator(-1),
        MaxValueValidator(10000)
    ])
    

    image = models.ImageField(upload_to='categories_photos/')
    
    def __str__(self):
        return self.name

class ProductStock(models.Model):
    """
    Модель продукта на складе, связывает продукт, цвет, и размер.
    """

    # планируется сделать валидацию наличия у продукта этого цвета и размера перед добавлением такой связи, ну ладно 
    
    product = models.ForeignKey(to="Product", on_delete=models.CASCADE, related_name='stock_items')
    
    color = models.ForeignKey(to="Color", on_delete=models.CASCADE)
    
    size = models.ForeignKey(to="Size", on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])  

    class Meta:
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        return f"{self.product.name} ({self.color.name}, {self.size.name}) — {self.quantity} шт."

    
    
    
class Product(models.Model):
    """класс модели продукта
    есть вариации и размеры
    тоесть те вариации и размеры которые подключенны через поля они описывают все возможные комбинации продукта
    а уже товары на складе будут описывать что есть а чего нету на данный момент"""
    
    # категория продукта 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    
    # пока что не оченб понятно как будет сделанно имя но пусть будет 
    name = models.CharField(max_length=50)
    
    description = models.TextField(max_length=500)
    
    # возмодные цвета продукта 
    colors = models.ManyToManyField('Color', related_name="products_with_color")
    # возможные размеры продукта 
    sizes = models.ManyToManyField("Size", related_name="products_with_size")
    
    #здест вообще должен быть список путей к фотграфиям продукта, но пока что не понятно как реализовыывать 
    
    def __str__(self):
        return self.name
    
    
class Color(models.Model):
    """
    класс модели расскраски 
    """
    
    name = models.CharField(max_length=15, unique=True)
    
    # фотграфия категории / пока что фотографии не реализую 
    # image = models.ImageField()
    
    def __str__(self):
        return self.name
    
class Size(models.Model):
    """
    класс модели размера 
    """
    
    name = models.CharField(max_length=15, unique=True)
    
    # фотграфия категории / пока что фотографии не реализую 
    # image = models.ImageField()
    
    def __str__(self):
        return self.name
