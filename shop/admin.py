# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import GoodsInfo, GoodsCategory, GoodsArea

# Register your models here.

@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    exclude = ["id"]

@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(GoodsArea)
class GoodsAreaAdmin(admin.ModelAdmin):
    pass
