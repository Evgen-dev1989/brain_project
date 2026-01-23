"""get the display resolution, screen diagonal and all the characteristics in general"""
import sys
import os
import re
import requests
from bs4 import BeautifulSoup


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


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

def characteristics(soup):
    try:
        display_block = None
        for block in soup.find_all("div", class_="br-pr-chr-item"):
            h3 = block.find("h3")
            if h3 and "Дисплей" in h3.text:
                display_block = block
                break

        if display_block:

            diagonal_div = None
            for div in display_block.find_all("div"):
                link = div.find("a")
                if link and "Діагональ екрану" in link.get("title", ""):
                    diagonal_div = div
                    break

            if diagonal_div:
                diagonal_value = diagonal_div.find("a").text.strip()
        
            else:
                print("Don't found div with title diagonal_value")

            resolution_div = None
            for div in display_block.find_all("div"):
                link = div.find("a")
                if link and "Роздільна здатність екрану" in link.get("title", ""):
                    resolution_div = div
                    break

            if resolution_div:
                display_resolution = resolution_div.find("a").text.strip()
            
            else:
                print("Don't found div with title resolution_value")

        else:
            print("Don't found display block")

        characteristics = {}

        for block in soup.find_all("div", class_="br-pr-chr-item"):

            category = block.find("h3").text.strip()
            characteristics[category] = {}

            for div in block.find_all("div"):
                spans = div.find_all("span")
                if len(spans) >= 2:
        
                    key = spans[0].text.strip()
                
                    value = spans[1].text.strip()
                
                    link = spans[1].find("a")
                    if link:
                        value = link.text.strip()

                    characteristics[category][key] = value

        phone = Phone.objects.create(
            
                screen_diagonal=diagonal_value,
                display_resolution=display_resolution,
                characteristics=characteristics,
                status="Done")
        if phone:
            print(f"screen diagonal: {phone.screen_diagonal}, "
                  f"{phone.display_resolution}, {phone.characteristics}")

    except Exception as e:
        print(f"Error: {e}")
