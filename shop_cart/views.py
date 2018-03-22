# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from .cache import CartCache
from django.contrib.auth.decorators import login_required

from shop.models import GoodsInfo


@login_required
def shop_cart(request):
    """购物车展示"""
    cartCache = CartCache(request.user)
    datas = cartCache.get_all()
    cart_info = []

    for gid, buy_num in datas.items():
        goods = GoodsInfo.objects.get(pk=gid)
        cart_info.append({
            "goods_info": goods,
            "buy_num": buy_num
        })

    return render(request, "shop_cart/cart.html", locals())


def add_cart(request, gid):
    """
    添加一个商品至购物车
        返回一个json的字符串,格式如下:
        {
            "code": 0
        }

        :param code 0 为成功完成
        :param code 1 为未登陆
        :param code -1 为失败
        :param code -2 参数错误

    """
    res = {
        "code": 0
    }

    # 验证是否登陆， 未登陆则跳回
    if not request.user.is_authenticated():
        res["code"] = 1
        return JsonResponse(res)

    cartCache = CartCache(request.user)

    goods_count = request.GET.get("buy_num")

    if gid and goods_count:
        cartCache.add_cart(gid, goods_count)
        datas = cartCache.get_all()
        res["buy_num"] = len(datas.keys())
    else:
        res["code"] = -2
    return JsonResponse(res)



def del_cart(request, gid):
    res = {
        "code": 0
    }

    # 验证是否登陆， 未登陆则跳回
    if not request.user.is_authenticated():
        res["code"] = 1
        return JsonResponse(res)

    cartCache = CartCache(request.user)
    cartCache.del_cart(gid)
    return JsonResponse(res)


def update_cart(request, gid):
    oper = request.GET.get("oper")
    buy_num = request.GET.get("buy_num")

    res = {
        "code": 0
    }

    # 验证是否登陆， 未登陆则跳回
    if not request.user.is_authenticated():
        res["code"] = 1
        return JsonResponse(res)

    cartCache = CartCache(request.user)
    cartCache.update_cart(gid, oper, buy_num=buy_num)
    res["buy_num"] = buy_num
    return JsonResponse(res)



