# Generated by Django 4.1.7 on 2023-02-28 12:12

import csv
import os
from pathlib import Path

from django.db import migrations


def add_ingredients(apps, schema_edition):
    path = Path(__file__).resolve().parent.parent.parent
    file = os.path.join(path, 'data\\ingredients.csv')
    model = apps.get_model(
        app_label='api',
        model_name='Ingredient'
    )
    with open(encoding='utf-8', file=file, mode='r') as csv_file:
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


def remove_ingredients(apps, schema_edition):
    path = Path(__file__).resolve().parent.parent.parent
    file = os.path.join(path, 'data\\ingredients.csv')
    model = apps.get_model(
        app_label='api',
        model_name='Ingredient'
    )
    with open(encoding='utf-8', file=file, mode='r') as csv_file:
        iterator = csv.reader(csv_file, delimiter=',')
        for item in iterator:
            model.objects.get(name=item[0]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=add_ingredients,
            reverse_code=remove_ingredients
        )
    ]