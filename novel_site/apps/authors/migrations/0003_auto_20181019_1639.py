# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-19 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_auto_20181012_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='名称'),
        ),
    ]