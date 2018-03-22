# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render, redirect
from shop_cart.cache import CartCache
from shop.models import GoodsInfo
from account.models import Receiver

from .models import OrderMain, OrderDetail
from django.db import transaction
from django.db.models import F
from shop_cart.cache import CartCache
from utils.decorators import login_required_ajax


import uuid

@login_required
@transaction.atomic
def show_order(request):
    if request.method == "POST":
        cart_by_goods_id = request.POST.getlist("cart_by_goods_id")

        # 数据验证， 因为没有500错误页面，暂时用/error/替代
        if not cart_by_goods_id:
            return HttpResponseRedirect("/error/")
        _goods_cart_map = {}

        cartCache = CartCache(request.user)
        for goods_id in cart_by_goods_id:
            _goods_cart_map[goods_id] = cartCache.get_one(goods_id)

        sid = transaction.savepoint()

        try:
            orderMain = OrderMain()
            orderMain.uuid = uuid.uuid4().__str__()
            orderMain.user = request.user
            if request.user.receiver_id:
                orderMain.receiver_id = request.user.receiver_id
            orderMain.save()

            for gid, buy_num in _goods_cart_map.items():
                orderDetail = OrderDetail()
                orderDetail.order = orderMain
                goods_info = GoodsInfo.objects.get(pk=gid)
                orderDetail.goods_info = goods_info
                orderDetail.goods_price = goods_info.price
                goods_total = goods_info.price * int(buy_num)
                orderDetail.goods_total = goods_total
                orderDetail.count = buy_num
                orderDetail.save()

            transaction.savepoint_commit(sid)
        except Exception, e:
            transaction.savepoint_rollback(sid)
            raise e
        return redirect("/shop_order/show_order/?order_id=%s" % orderMain.id)

    order_id = request.GET.get("order_id")
    orderDetails = OrderDetail.objects.filter(order__id=order_id)
    order = OrderMain.objects.get(pk=order_id)

    if order.is_pay != "0":
        message = u"非法请求"
        return render(request, "shop_order/message.html", locals())

    receivers = Receiver.objects.get(user=order.user)
    return render(request, "shop_order/place_order.html", locals())

@login_required
@transaction.atomic
def order(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = OrderMain.objects.get(pk=order_id)

        if order.is_pay != "0":
            message = u"非法请求"
            return render(request, "shop_order/message.html", locals())

        orderDetails = OrderDetail.objects.filter(order__id=order_id)
        cartCache = CartCache(request.user)
        sid = transaction.savepoint()

        try:
            total = 0
            for od in orderDetails:
                if od.goods_info.stock < od.count:
                    message = u"库存不足"
                    return render(request, "shop_order/message.html", locals())
                od.goods_info.stock = F("stock") - od.count
                od.goods_info.save()
                # 这里需要使用事务完成，与mysql的事务相结合，这里留做作业
                cartCache.del_cart(od.goods_info.id)
                total += od.goods_total

            order.is_pay = "1"
            order.total = total
            order.save()


            transaction.savepoint_commit(sid)
        except Exception, e:
            transaction.savepoint_rollback(sid)
            raise e

    # 提交成功应该跳转支付页面，因为支付这块暂时没有，这里直接跳转订单提交成功
    message = u"提交成功"
    return render(request, "shop_order/message.html", locals())


@login_required_ajax
def cannel_order(request):
    res = {
        "code": 0
    }
    order_id = request.GET.get("order_id")
    order = OrderMain.objects.get(pk=order_id)
    order.is_pay = "-1"
    order.save()
    return JsonResponse(res)