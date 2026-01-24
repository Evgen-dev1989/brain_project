"""get data from soup and write to data model Phone"""
import sys
import os
import re
import requests
from bs4 import BeautifulSoup
import csv
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'brain_project', 'parser_app'))
sys.path.append(BASE_DIR)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'brain_project')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'brain_project', 'parser_app')))
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brain_project.settings')
django.setup()


import modules.load_django
from parser_app.models import Phone
from get_characteristics import characteristics
from get_links_photo import get_link_photos




def get_data(soup):

    try:
        title_tag = soup.find("h1", class_="main-title")
        if title_tag:
            product_name = title_tag.text.strip()
        print(f"product name: {product_name}")

    except AttributeError as e:
        print(f"Error extracting product name: {e}")
        product_name = None
        
    try:
        colors = []
        for color_div in soup.select('.series-item.series-color'):
            a_tag = color_div.find('a')
            if a_tag and a_tag.has_attr('href'):
                url = a_tag['href']
                match = re.search(r'iPhone_16_Pro_Max_256GB_([A-Za-z_]+)-p', url)
                if match:
                    color = match.group(1).replace('_', ' ')
               
                    colors.append(color)
        print(f"Colors: {colors}")

    except AttributeError as e:
        print(f"Error extracting colors: {e}")
        colors  = None

    try:
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
        print(f"Memory Capacity: {memory_capacity}")
    except AttributeError as e:
        print(f"Error extracting memory capacity: {e}")
        memory_capacity = None

    try:
        manufacturer = None
        for span in soup.find_all('span'):
            if span.text.strip() == 'Виробник':
                next_span = span.find_next('span')
                if next_span:
                    manufacturer = next_span.text.strip()
                    break
        print(f"Manufacturer: {manufacturer}")
    except AttributeError as e:
        print(f"Error extracting price: {e}")
        manufacturer = None
    
    try:
        for price in soup.find("div", class_="price-wrapper"):
            if price:
                price = price.find_next('span').text.strip()
                break
        print(f"Price: {price}")
    except AttributeError as e:
        print(f"Error extracting price: {e}")   
        price  = None





    try:
        product_code_div = soup.find("div", class_="br-pr-code br-code-block")
        if product_code_div:
    
            product_code_span = product_code_div.find("span", class_="br-pr-code-val")
            if product_code_span:
                product_code = product_code_span.text.strip()

            else:
                print("don't found span with class 'br-pr-code")
        else:
            print("don't found div with class 'br-pr-code br-code-block")
        print(f"Product Code: {product_code}")
    except AttributeError as e:
        print(f"Error extracting product code: {e}")
        product_code = None


    try:
        number_of_reviews = soup.find("div", class_="fast-navigation-comments-body")
        if number_of_reviews:

            number_of_reviews_span = number_of_reviews.find('a')
        
            if number_of_reviews_span:
                number_of_reviews = number_of_reviews_span.text.strip()
            
            else:
                print(" don`t found span number_of_reviews_span")
        else:
            print("don't found number_of_reviews")
        print(f"Number of Reviews: {number_of_reviews}")
    except AttributeError as e:
        print(f"Error extracting number of reviews: {e}")
        number_of_reviews = None




    try:    
        phone, created = Phone.objects.get_or_create(
            product_code=product_code,
            defaults={
                'product_name': product_name,
                'number_of_reviews': number_of_reviews,
                'price': price,
                'manufacturer': manufacturer,
                'memory_capacity': memory_capacity,
                'colors': colors
            }
        )

        if not created:
       
            phone.product_name = product_name
            phone.number_of_reviews = number_of_reviews
            phone.price = price
            phone.manufacturer = manufacturer
            phone.memory_capacity = memory_capacity
            phone.colors = colors
            phone.save()
    except AttributeError as e:
        print(f"Error saving to database: {e}")
        value = None


def main():

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

    get_data(soup)
    get_link_photos(soup)
    characteristics(soup)
 

if __name__ == "__main__":
    main()


   


    # output_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'result_brain_project.csv')
    # output_path = os.path.abspath(output_path)

    # fieldnames = [
    #     'product_name', 'colors', 'memory_capacity', 'manufacturer', 'price', 'promotional_price',
    #     'product_code', 'number_of_reviews', 'screen_diagonal', 'display_resolution',
    #     'characteristics', 'photos', 'link', 'status'
    # ]

    # with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for phone in Phone.objects.all():
    #         writer.writerow({
    #             'product_name': phone.product_name,
    #             'colors': json.dumps(phone.colors, ensure_ascii=False),
    #             'memory_capacity': json.dumps(phone.memory_capacity, ensure_ascii=False),
    #             'manufacturer': phone.manufacturer,
    #             'price': phone.price,
    #             'promotional_price': phone.promotional_price,
    #             'product_code': phone.product_code,
    #             'number_of_reviews': phone.number_of_reviews,
    #             'screen_diagonal': phone.screen_diagonal,
    #             'display_resolution': phone.display_resolution,
    #             'characteristics': json.dumps(phone.characteristics, ensure_ascii=False),
    #             'photos': json.dumps(phone.photos, ensure_ascii=False),
    #             'link': phone.link,
    #             'status': phone.status,
    #         })




