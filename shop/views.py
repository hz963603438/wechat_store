# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from .models import GoodsInfo, GoodsCategory
from django.views.decorators.cache import cache_page

from django.core.paginator import Paginator
from django.db.models import F

from .cache import BrowseCache


def index(request):
    goods_list = []

    categorys = GoodsCategory.objects.filter(status=0).all()

    for c in categorys:
        goodsinfos = GoodsInfo.objects.filter(category=c).order_by("-id")[:4]
        goods_list.append({
            "goods_category": c,
            "goodsinfos": goodsinfos
        })

    return render(request, "shop/index.html", locals())


def categorys(request, cid):
    """
        使用分页查询种类商品列表
    """
    # 获取需要跳转的页码，如果未获取到，默认为第一页
    curr_page = int(request.GET.get("curr_page", 1))

    # 排序规则
    curr_order = request.GET.get("curr_order", "1")

    order_map = {
        "1": "id",
        "2": "price",
        "3": "click_count"
    }

    # 使用分类查询商品
    current_goods_obj = GoodsInfo.objects.filter(
        category_id=cid).order_by("-%s" % order_map[curr_order])

    # 使用django Paginator 进行分页， 这里页面展示5个
    p = Paginator(current_goods_obj, 5)
    page = p.page(curr_page)

    # 传递分页的参数
    params = {"cid": cid}

    return render(request, "shop/list.html", locals())


def detail(request, gid):
    goods_info = GoodsInfo.objects.get(pk=gid)

    if request.user.is_authenticated():
        browses = BrowseCache.get_browse(request.user)
        if gid not in browses:
            BrowseCache.set_browse(request.user, gid)
            GoodsInfo.objects.filter(pk=gid)    \
                        .update(click_count=F('click_count') + 1)

    return render(request, "shop/detail.html", locals())
