import csv
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

FILE_DIR = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    """
    Command to load ingredient's fixtures.
    Fixture must be located at data directory next to manage.py file.
    Use: python manage.py importcsv <file>
    """
    help = 'Заполнение модели объектами из выбранного файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            help='Имя csv-файла',
            type=str
        )

    def handle(self, *args, **options):
        file_path = os.path.join(FILE_DIR, options['file'])
        model = apps.get_model(
            app_label='api',
            model_name='Ingredient'
        )
        with open(encoding='utf-8', file=file_path, mode='r') as csv_file:
            iterator = csv.reader(csv_file, delimiter=',')
            objs = []
            data_empty = False
            while not data_empty:
                try:
                    objs.clear()
                    for _ in range(100):
                        row = next(iterator)
                        kwargs = {'name': row[0], 'measurement_unit': row[1]}
                        objs.append(model(**kwargs))
                except StopIteration:
                    data_empty = True
                finally:
                    model.objects.bulk_create(objs=objs)
