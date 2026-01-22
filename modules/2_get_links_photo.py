import sys
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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

try:

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)


    url = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"
    driver.get(url)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "br-prs-f")))

    except:
        print("Don't wait for loading page")


    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    link_photos = []
    photo_div = soup.find("div", class_="br-prs-f main-pictures-block slick-initialized slick-slider slick-vertical")
    if photo_div:
        
        for img_tag in photo_div.find_all("img"):
            if img_tag.has_attr("src"):
                link_photos.append(img_tag["src"])
            elif img_tag.has_attr("data-observe-src"):
                link_photos.append(img_tag["data-observe-src"])
    else:
        print('Don`t found div with class "br-prs-f main-pictures-block slick-initialized slick-slider slick-vertical"')
       
    link_photos = list(dict.fromkeys(link_photos))


    if link_photos:
        phone = Phone.objects.create(
            name="Apple iPhone 16 Pro Max 256GB Black Titanium",
            photos=link_photos,
            status="Done"
    )
    else:
        print("No photos found, Phone object not created.")

except Exception as e:
    print(f"Error: {e}")