# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-12 11:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter0',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表0',
                'verbose_name_plural': '小说章节表0',
                'db_table': 'tb_chapter_0',
            },
        ),
        migrations.CreateModel(
            name='Chapter1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表1',
                'verbose_name_plural': '小说章节表1',
                'db_table': 'tb_chapter_1',
            },
        ),
        migrations.CreateModel(
            name='Chapter2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表2',
                'verbose_name_plural': '小说章节表2',
                'db_table': 'tb_chapter_2',
            },
        ),
        migrations.CreateModel(
            name='Chapter3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表3',
                'verbose_name_plural': '小说章节表3',
                'db_table': 'tb_chapter_3',
            },
        ),
        migrations.CreateModel(
            name='Chapter4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表4',
                'verbose_name_plural': '小说章节表4',
                'db_table': 'tb_chapter_4',
            },
        ),
        migrations.CreateModel(
            name='Chapter5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表5',
                'verbose_name_plural': '小说章节表5',
                'db_table': 'tb_chapter_5',
            },
        ),
        migrations.CreateModel(
            name='Chapter6',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表6',
                'verbose_name_plural': '小说章节表6',
                'db_table': 'tb_chapter_6',
            },
        ),
        migrations.CreateModel(
            name='Chapter7',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表7',
                'verbose_name_plural': '小说章节表7',
                'db_table': 'tb_chapter_7',
            },
        ),
        migrations.CreateModel(
            name='Chapter8',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表8',
                'verbose_name_plural': '小说章节表8',
                'db_table': 'tb_chapter_8',
            },
        ),
        migrations.CreateModel(
            name='Chapter9',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_url', models.URLField(max_length=255, unique=True, verbose_name='章节链接')),
                ('chapter_index', models.PositiveIntegerField(default=0, verbose_name='章节顺序')),
                ('chapter_name', models.CharField(max_length=255, verbose_name='章节名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说章节表9',
                'verbose_name_plural': '小说章节表9',
                'db_table': 'tb_chapter_9',
            },
        ),
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('novel_name', models.CharField(max_length=32, unique=True, verbose_name='小说名称')),
                ('site_name', models.CharField(max_length=32, verbose_name='小说网站')),
                ('url', models.CharField(max_length=255, unique=True, verbose_name='小说链接')),
                ('image', models.ImageField(default='default_novel.jpg', max_length=200, upload_to='novel/', verbose_name='小说图片')),
                ('intro', models.CharField(default='', max_length=255, verbose_name='小说简介')),
                ('detail', models.TextField(default='', verbose_name='详细介绍')),
                ('read_nums', models.PositiveIntegerField(default=0, verbose_name='阅读数')),
                ('fav_nums', models.PositiveIntegerField(default=0, verbose_name='收藏数')),
                ('parser', models.CharField(default='biqugeParser', max_length=255, verbose_name='内容解析器')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.Author', verbose_name='小说作者')),
            ],
            options={
                'verbose_name': '小说',
                'verbose_name_plural': '小说',
                'db_table': 'tb_novel',
            },
        ),
        migrations.CreateModel(
            name='NovelCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='分类名称')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '小说分类',
                'verbose_name_plural': '小说分类',
                'db_table': 'tb_novel_category',
            },
        ),
        migrations.AddField(
            model_name='novel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.NovelCategory', verbose_name='小说分类'),
        ),
        migrations.AddField(
            model_name='chapter9',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter8',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter7',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter6',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter5',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter4',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter3',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter2',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter1',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
        migrations.AddField(
            model_name='chapter0',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Novel', verbose_name='小说'),
        ),
    ]
