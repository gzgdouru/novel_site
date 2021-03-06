# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-12 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('intro', models.CharField(default='', max_length=255, verbose_name='简介')),
                ('detail', models.TextField(default='', verbose_name='详细介绍')),
                ('image', models.ImageField(default='default.jpg', max_length=200, upload_to='authors/', verbose_name='作者图片')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说作者',
                'verbose_name_plural': '小说作者',
                'db_table': 'tb_novel_author',
            },
        ),
    ]
