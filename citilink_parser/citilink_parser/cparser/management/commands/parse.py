import requests
from bs4 import BeautifulSoup as bs4
import os
from django.core.management.base import BaseCommand
from cparser.models import Product, Category
from django.db import IntegrityError
from django.conf import settings


class CitilinkParser:

    def __init__(self):
        self.url = 'https://www.citilink.ru/catalog/televizory'

    def parse(self):
        r = requests.get(self.url)
        soup = bs4(r.text, 'lxml')
        try:
            category = soup.find('h1', class_='Heading Heading_level_1 Subcategory__title js--Subcategory__title').text.strip()
            Category(name=category).save()
            print(category)
            count_pages = int(soup.find_all('a', class_='PaginationWidget__page')[-1].text.strip())
            img_paths = []
            for page in range(1, count_pages + 1):
                url = f'{self.url}/?p={page}'
                r = requests.get(url)
                soup = bs4(r.text, 'lxml')
                all_products = soup.find_all(
                    'div',
                    class_='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist'
                )
                for p in all_products:
                    name = p.find('a', class_='ProductCardHorizontal__title Link js--Link Link_type_default').text
                    print(name)
                    price = p.find('span',
                                   class_='ProductCardHorizontal__price_current-price js--ProductCardHorizontal__price_current-price')
                    if price is None:
                        price = None
                    else:
                        price = int(price.text.replace(' ', ''))
                    print(price)
                    img = p.find('img')['src']
                    print(img)
                    img_paths.append(img)
                    Product(name=name, price=price, image=img, category=Category.objects.get(name=category)).save()
            print('Товары успешно получены!')
            self.upload_images(img_paths, category)
        except IntegrityError:
            print(f'Товары из категории \'{category}\' Вы уже получали!')

    @staticmethod
    def upload_images(paths: list, subdir: str) -> None:
        print('Загрузка изображений началась ...')
        folder = settings.MEDIA_ROOT + '/upload/'
        if not os.path.exists(folder + subdir):
            os.mkdir(folder + subdir)
            for path in paths:
                filename = path.split('/')[-1]
                img_data = requests.get(path, verify=True).content
                with open(folder + subdir + '/' + filename, 'wb') as handler:
                    handler.write(img_data)
                print(filename + ' загружено')
        print('Загрузка изображений завершилась.')


class Command(BaseCommand):
    help = 'Ситилинк парсер'

    def handle(self, *args, **options):
        p = CitilinkParser()
        p.parse()
