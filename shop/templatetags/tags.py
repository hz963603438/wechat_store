#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-13 21:34:35
# @Author  : kevin (wuhao@idvert.com)

from django import template

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from shop.models import GoodsInfo
from django.conf import settings

import urlparse
import urllib

register = template.Library()


@register.simple_tag
def divide_page(curr_page, page_obj, url_name, request_url, page_name="", args=(), kwargs={}):
    """
        算法
            1、先获取所有页码列表
            range_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            2、 然后定义需要展示的数目，这里定义为一个5
            max_page_count = 5

            3、获取中间位置前后需要加减索引
            center_index = max_page_count / 2

            4、获取当前页面索引，这里定义为当前页面为5
            curr_index = range_list.index(5)
            range_list[curr_index-center_index:]
            [3, 4, 5, 6, 7, 8, 9]

            5、循环处理右边
            获取一个计数器
            当计数器的索引大于总数目时退出
            [3, 4, 5, 6, 7, 8, 9] 迭代这个时
            当迭代到7的位置，计数器的值就为6，退出循环，就获取到以下列表
            [3, 4, 5, 6, 7]

    """
    url = reverse(url_name, args=args, kwargs=kwargs)       # 点击页码需要跳转的url前缀
    # 默认为unicode,这里修改为utf8
    url = url.encode("utf8")
    page_str = '<div class="pagenation">'
    max_page_count = 5
    page = page_obj.page(curr_page)

    # 获取当前get参数
    params = {k.encode("utf8"): v[0].encode("utf8") for k, v in urlparse.parse_qs(
        urlparse.urlparse(request_url).query).items()}

    if not page_name:
        page_name = "curr_page"

    # 生成上一页html
    if page.has_previous():
        params[page_name] = curr_page - 1

        curr_url = "%s?%s" % (url, urllib.urlencode(params))
        page_str += '<a href="%s" style="background-color: #5bc0de"> 上一页 </a>' % curr_url

    center_index = max_page_count / 2
    page_range = [c for c in page_obj.page_range]
    page_index = page_range.index(curr_page)

    if page_index >= center_index:
        page_range = page_range[page_index-center_index:]

    i = 1
    # 生成中间页码html
    for cp in page_range:
        params[page_name] = cp
        curr_url = "%s?%s" % (url, "&".join(["%s=%s" % (k,v) for k,v in params.items()]))
        # curr_url = "%s?%s" % (url, urllib.urlencode(params))
        if cp == curr_page:
            page_str += '<a href="%s" class="active" style="background-color: #1b6d85">%s</a>' % (
                curr_url, cp)
        else:
            page_str += '<a href="%s" >%s</a>' % (
                curr_url, cp)

        i += 1
        if i > max_page_count:
            break

    # 生成下一页html
    if page.has_next():
        params[page_name] = curr_page + 1
        curr_url = "%s?%s" % (url, urllib.urlencode(params))
        page_str += '<a href="%s" style="background-color: #5bc0de"> 下一页 </a>' % curr_url

    page_str += "</div>"

    return mark_safe(page_str)



@register.inclusion_tag("shop/refferral_good.html")
def refferral_goods(cid=None):
    if cid:
        refferral_goods = GoodsInfo.objects.filter(category_id=cid).order_by("-id")[:2]
    else:
        refferral_goods = GoodsInfo.objects.all().order_by("-id")[:2]

    return {
        "refferral_goods": refferral_goods,
        "MEDIA_URL": settings.MEDIA_URL
    }

