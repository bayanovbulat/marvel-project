# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-23 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComicModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('release_date', models.DateField(verbose_name='Дата выхода')),
                ('ean', models.CharField(max_length=25, verbose_name='EAN')),
                ('type', models.CharField(max_length=25, verbose_name='Варианты выхода')),
                ('cover', models.ImageField(upload_to='app/static/pictures')),
                ('in_stock', models.BooleanField(default=False, editable=False, verbose_name='Выбрать комикс')),
            ],
            options={
                'verbose_name': 'Comic',
                'verbose_name_plural': 'Comics',
                'ordering': ['name', 'release_date'],
            },
        ),
    ]
