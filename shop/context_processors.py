#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-13 20:48:33
# @Author  : kevin (wuhao@idvert.com)


from .models import GoodsCategory

def category_list(request):
	category_list = GoodsCategory.objects.filter(status=0).all()
	return {"category_list": category_list}