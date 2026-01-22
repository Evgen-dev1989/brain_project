""" ипортируем модель Book и выводим все объекты из базы данных """
import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'jek_project', 'parser_app'))
sys.path.append(BASE_DIR)

import modules.load_django

from parser_app.models import Book

book = Book.objects.all()
for i in book:
    print(i)




