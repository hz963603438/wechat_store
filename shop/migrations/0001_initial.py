# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 08:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u5546\u54c1\u4ea7\u5730')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u5546\u54c1\u4ea7\u5730',
                'verbose_name_plural': '\u5546\u54c1\u4ea7\u5730',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u5546\u54c1\u5206\u7c7b\u540d')),
                ('status', models.IntegerField(choices=[(0, '\u6b63\u5e38'), (1, '\u5220\u9664')], default=0, verbose_name='\u72b6\u6001')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u5546\u54c1\u5206\u7c7b',
                'verbose_name_plural': '\u5546\u54c1\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u5546\u54c1\u540d\u79f0')),
                ('images', models.ImageField(upload_to='goods/%Y/%m/%d', verbose_name='\u5546\u54c1\u56fe\u7247\u5730\u5740')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u5546\u54c1\u4ef7\u683c')),
                ('unit', models.CharField(max_length=10, verbose_name='\u5546\u54c1\u5355\u4f4d')),
                ('status', models.IntegerField(choices=[(0, '\u6b63\u5e38'), (1, '\u5220\u9664')], default=0, verbose_name='\u72b6\u6001')),
                ('description', models.TextField(verbose_name='\u5546\u54c1\u63cf\u8ff0')),
                ('stock', models.IntegerField(verbose_name='\u5546\u54c1\u5e93\u5b58')),
                ('detail', tinymce.models.HTMLField()),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.GoodsArea', verbose_name='\u5546\u54c1\u4ea7\u5730')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.GoodsCategory', verbose_name='\u5546\u54c1\u5206\u7c7b')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u5546\u54c1\u4fe1\u606f',
                'verbose_name_plural': '\u5546\u54c1\u4fe1\u606f',
            },
        ),
    ]