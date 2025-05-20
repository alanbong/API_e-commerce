import csv
import os

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.conf import settings
# from shop_backend.settings import BASE_DIR

from io import BytesIO

from categories.models import Category, SubCategory
from products.models import Product


def load_image(relative_path):
    '''
    Загружает изображение из папки media.
    '''
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f'Изображение не найдено: {full_path}')
    with open(full_path, 'rb') as f:
        content = f.read()
    return ImageFile(BytesIO(content), name=os.path.basename(full_path))


def create_category(row):
    '''
    Создаёт объект Category из строки CSV.
    row: [name, slug, image_path]
    '''
    Category.objects.get_or_create(
        name=row[0],
        slug=row[1],
        defaults={
            'image': load_image(row[2])
        }
    )


def create_subcategory(row):
    '''
    Создаёт объект SubCategory из строки CSV.
    row: [name, slug, image_path, category_slug]
    '''
    category = Category.objects.get(slug=row[3])
    SubCategory.objects.get_or_create(
        name=row[0],
        slug=row[1],
        category=category,
        defaults={
            'image': load_image(row[2])
        }
    )


def create_product(row):
    '''
    Создаёт объект Product из строки CSV.
    row: [name, slug, description, price, image_path, subcategory_slug]
    '''
    subcategory = SubCategory.objects.get(slug=row[5])
    Product.objects.get_or_create(
        name=row[0],
        slug=row[1],
        defaults={
            'description': row[2],
            'price': row[3],
            'image': load_image(row[4]),
            'subcategory': subcategory,
            'category': subcategory.category,
        }
    )


# Указываем соответствие CSV-файлов и функций обработки строк
ACTION_MAP = {
    'categories.csv': create_category,
    'subcategories.csv': create_subcategory,
    'products.csv': create_product,
}


class Command(BaseCommand):
    '''
    Команда Django для импорта данных из CSV-файлов в базу данных.
    Расположение файлов:
    - .csv: в директории data/
    - Изображения: в media/.
    '''
    help = 'Загружает данные из CSV-файлов.'

    def handle(self, *args, **options):
        '''
        Загружает все CSV файлы.
        '''
        data_dir = os.path.join(settings.BASE_DIR, 'data')

        for filename, process_function in ACTION_MAP.items():
            file_path = os.path.join(data_dir, filename)

            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(
                    f"Файл {filename} не найден, пропускаем."
                ))
                continue

            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    process_function(row)

            self.stdout.write(self.style.SUCCESS(
                f"Файл {filename} успешно загружен!"
            ))
