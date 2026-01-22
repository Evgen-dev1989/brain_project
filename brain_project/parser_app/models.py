from django.db import models
from django.contrib.postgres.fields import ArrayField



class Phone(models.Model):
    # 1. Основные данные (важные поля)
    name = models.CharField(max_length=255, null=True)
    colors = models.CharField(max_length=255, null=True)   
    memory_capacity = models.CharField(max_length=255, null=True)   
    manufacturer = models.CharField(max_length=255, null=True)   
    price = models.CharField(max_length=100, null=True)    
    promotional_price = models.CharField(max_length=100, null=True)      
    product_code = models.CharField(max_length=255, null=True)  
    number_of_reviews = models.CharField(max_length=255, null=True)   
    screen_diagonal = models.CharField(max_length=255, null=True)         
    display_resolution = models.CharField(max_length=50, null=True)       
    characteristics = models.CharField(null=True)                     


    photos = ArrayField(models.URLField(max_length=500, null=True), null=True, blank=True, help_text="Ссылки на все фото товара")  # Все фото товара
    characteristics = models.TextField(null=True, blank=True)   
    link = models.URLField(null=True, blank=True)            
    status = models.CharField(max_length=50, default="New", null=True)  # Статус обработки: New → Done

    def __str__(self):
        return self.name
    



# Характеристики товара. Все характеристики на вкладке. Характеристики собрать как словарь




# python manage.py makemigrations

# python manage.py migrate