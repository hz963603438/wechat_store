#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-13 20:48:33
# @Author  : kevin (wuhao@idvert.com)

from .cache import CartCache

def goods_num(request):
    goods_num = 0
    if request.user.is_authenticated():
        cartCache = CartCache(request.user)
        datas = cartCache.get_all()
        goods_num = len(datas.keys())
    return {"goods_num": goods_num}