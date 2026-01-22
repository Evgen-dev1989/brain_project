"""Файл обращаеться к сайту и собирает информацию с каждого товара на странице, сохраняем все в модель Thing."""
import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Исправленный путь к parser_app
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'brain_project', 'parser_app'))
sys.path.append(BASE_DIR)

import modules.load_django

from parser_app.models import Phone



url = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1', 
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'Trailers', 
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

phone = Phone.objects.all()


try:
    title_tag = soup.find("h1", class_="main-title")
    if title_tag:
        product_name = title_tag.text.strip()
        #print(product_name)

    colors = []
    for color_div in soup.select('.series-item.series-color'):
        a_tag = color_div.find('a')
        if a_tag and a_tag.has_attr('href'):
            url = a_tag['href']
            match = re.search(r'iPhone_16_Pro_Max_256GB_([A-Za-z_]+)-p', url)
            if match:
                color = match.group(1).replace('_', ' ')
                colors.append(color)
    #print(colors)


    memory_capacity = []
    valid_memory_values = {"256 GB", "512 GB", "1 TB"} 

    for mem_div in soup.select('.series-item.series-characteristic'):

        if 'hidden' in mem_div.get('class', []):
            continue

        a_tag = mem_div.find('a')
        if a_tag and a_tag.get_text(strip=True):  
            text = a_tag.get_text(strip=True)

           
            match = re.search(r'^(\d+)\s*(GB|Tb|Gb|TB)$', text, re.IGNORECASE)
            if match:
                value = match.group(0).upper() 
                if value in valid_memory_values:  
                    memory_capacity.append(value)

    memory_capacity = list(dict.fromkeys(memory_capacity))
    #print(memory_capacity)


    manufacturer = None
    for span in soup.find_all('span'):
        if span.text.strip() == 'Виробник':
            next_span = span.find_next('span')
            if next_span:
                manufacturer = next_span.text.strip()
                break

    #print(f"manufacturer: {manufacturer}")

    for price in soup.find("div", class_="price-wrapper"):
        if price:
            price = price.find_next('span').text.strip()
            print(price)
            break
        

except AttributeError as e:
    print(f"Error extracting product name: {e}")
    




    # price = models.CharField(max_length=100, null=True)    
    # promotional_price = models.CharField(max_length=100, null=True)      
    # product_code = models.CharField(max_length=255, null=True)  
    # number_of_reviews = models.CharField(max_length=255, null=True)   
    # screen_diagonal = models.CharField(max_length=255, null=True)         
    # diisplay_resolution = models.CharField(max_length=50, null=True)       
    # characteristics = models.CharField(null=True)                     


    # photos = ArrayField(models.URLField(max_length=500, null=True), null=True, blank=True, help_text="Ссылки на все фото товара")  # Все фото товара
    # characteristics = models.TextField(null=True, blank=True)   
    # link = models.URLField(null=True, blank=True)            
    # status = models.CharField(max_length=50, default="New", null=True)  # Статус обработки: New → Done

    # item.save()