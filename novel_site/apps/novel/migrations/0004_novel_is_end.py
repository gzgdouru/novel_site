# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-17 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0003_novel_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='is_end',
            field=models.BooleanField(default=False, verbose_name='是否已完结'),
        ),
    ]