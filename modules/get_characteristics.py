"""get the display resolution, screen diagonal and all the characteristics in general"""
import sys
import os
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

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


def clean_value(val):
    import re
    if isinstance(val, str):
        cleaned = val.replace('\xa0', ' ')
        cleaned = re.sub(r'[ \t]+', ' ', cleaned) 
        cleaned = re.sub(r'\n+', '\n', cleaned)   
        cleaned = re.sub(r' *, *', ', ', cleaned)   
        return cleaned.strip()
    if isinstance(val, dict):
        return {k: clean_value(v) for k, v in val.items()}
    return val

def characteristics(soup):

    try:
        display_block = None

        for block in soup.find_all("div", class_="br-pr-chr-item"):
            h3 = block.find("h3")
            if h3 and re.search(r"диспле[йя]|display", h3.text, re.IGNORECASE):
                display_block = block
                break

        if display_block:


            try:
                diagonal_div = None

                for div in display_block.find_all("div"):
                    link = div.find("a")
                    if link and re.search(r"диагонал|diagonal", link.get("title", ""), re.IGNORECASE):
                        diagonal_div = div
                        break

                if diagonal_div:
                    diagonal_value = diagonal_div.find("a").text.strip()
                else:
                    print("Don't found div with title diagonal_value")

            except AttributeError as e:
                print(f"Error finding diagonal value: {e}")
                diagonal_value = None


            try:
                resolution_div = None
        
                for div in display_block.find_all("div"):
                    link = div.find("a")
                    if link and re.search(r"разреш|роздільн|resolution", link.get("title", ""), re.IGNORECASE):
                        resolution_div = div
                        break

                if resolution_div:
                    display_resolution = resolution_div.find("a").text.strip()
                else:
                    print("Don't found div with title resolution_value")
            except AttributeError as e:
                print(f"Error finding resolution value: {e}")
                display_resolution = None





            else:
                print("Don't found display block")
        
            try:
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

            except AttributeError as e:
                print(f"Error finding characteristics value: {e}")
                characteristics = None
   
        characteristics_clean = clean_value(characteristics)
        phone = Phone.objects.create(
            screen_diagonal=diagonal_value,
            display_resolution=display_resolution,
            characteristics=characteristics_clean,
            status="Done"
        )
        if phone:
            from pprint import pprint
            print(f"screen diagonal: {phone.screen_diagonal}")
            print(f"display_resolution: {phone.display_resolution}")
            print("characteristics:")
            pprint(phone.characteristics, sort_dicts=False, width=120)

    except Exception as e:
        print(f"Error: {e}")
