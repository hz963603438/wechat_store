# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from tinymce.models import HTMLField

# Create your models here.


class GoodsCategory(models.Model):
    STATUS = (
        (0, "正常"),
        (1, "删除")
    )
    name = models.CharField(max_length=20, verbose_name="商品分类名")
    status = models.IntegerField(choices=STATUS, default=0, verbose_name='状态')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __str__(self):
        return self.name.encode("utf8")


class GoodsArea(models.Model):
    name = models.CharField(max_length=20, verbose_name='商品产地')

    class Meta:
        verbose_name = '商品产地'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __str__(self):
        return self.name.encode("utf8")


class GoodsInfo(models.Model):
    """
        商品类
    """
    STATUS = (
        (0, "正常"),
        (1, "删除")
    )

    name = models.CharField(max_length=30, verbose_name="商品名称")
    images = models.ImageField(
        upload_to='goods/%Y/%m/%d', verbose_name='商品图片地址')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='商品价格')
    click_count = models.IntegerField(default=0, verbose_name='商品点击量')
    unit = models.CharField(max_length=10, verbose_name='商品单位')
    status = models.IntegerField(choices=STATUS, default=0, verbose_name='状态')
    description = models.TextField(verbose_name='商品描述')
    stock = models.IntegerField(verbose_name='商品库存')
    detail = HTMLField(verbose_name='商品详情')
    category = models.ForeignKey('GoodsCategory', verbose_name='商品分类')
    area = models.ForeignKey('GoodsArea', verbose_name='商品产地', null=True)

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __str__(self):
        return self.name.encode("utf8")
