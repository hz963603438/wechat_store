# -*- coding: utf-8 -*-

from django.db import models
from account.models import UserProfile
from shop.models import GoodsInfo
from account.models import Receiver


class OrderMain(models.Model):
    order_statue = (
        ('-1', '取消'),
        ('0', '创建'),
        ('1', '未支付'),
        ('2', '已支付'),
        ('3', '已发货'),
        ('4', '待发货'),
    )

    uuid = models.CharField(max_length=50, unique=True,verbose_name='订单编号')
    order_time = models.DateTimeField(auto_now_add=True, verbose_name='提交订单时间')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='付款时间')
    user = models.ForeignKey(UserProfile, verbose_name='购买的用户')
    total = models.DecimalField(null=True, max_digits=8, decimal_places=2, verbose_name='总价格')
    is_pay = models.CharField(max_length=5, choices=order_statue, default="0", verbose_name='订单状态')
    receiver = models.ForeignKey(Receiver, default=None, verbose_name="收货详情")

    class Meta:
        verbose_name = '订单中心'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

    def __str__(self):
        return str(self.user) + str(self.order_id)


class OrderDetail(models.Model):
    order = models.ForeignKey(OrderMain, verbose_name='订单中心')
    goods_info = models.ForeignKey(GoodsInfo, verbose_name='商品')
    goods_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='商品价格')
    goods_total = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='商品价格')
    count = models.IntegerField(verbose_name='购买商品的数量')

    class Meta:
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

    def __str__(self):
        return str(self.order) + str(self.goods_info)

