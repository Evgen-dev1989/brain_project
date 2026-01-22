from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField



class Phone(models.Model):
    # 1. Основные данные (важные поля)
    product_name = models.CharField(max_length=255, null=True)
    colors = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    memory_capacity = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True)   
    price = models.CharField(max_length=100, null=True)    
    promotional_price = models.CharField(max_length=100, null=True)      
    product_code = models.CharField(max_length=255, null=True)  
    number_of_reviews = models.CharField(max_length=255, null=True)   
    screen_diagonal = models.CharField(max_length=255, null=True)         
    display_resolution = models.CharField(max_length=50, null=True)       
    characteristics = JSONField(null=True, blank=True)                   


    photos = ArrayField(models.URLField(max_length=500, null=True), null=True, blank=True, help_text="Ссылки на все фото товара")  
    link = models.URLField(null=True, blank=True)            
    status = models.CharField(max_length=50, default="New", null=True)  # Статус обработки: New → Done

    def __str__(self):
        return self.name




# python manage.py makemigrations

# python manage.py migrate