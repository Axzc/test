# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('title', models.CharField(verbose_name='文章标题', max_length=200)),
                ('slug', models.CharField(verbose_name='文章概括', max_length=200)),
                ('text', tinymce.models.HTMLField(verbose_name='文章内容')),
                ('status', models.SmallIntegerField(verbose_name='文章状态', default=0, choices=[(0, '上线'), (1, '下线')])),
                ('image', models.ImageField(upload_to='image')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
