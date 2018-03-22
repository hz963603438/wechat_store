# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    """用户信息"""
    gender_type = (
        ("0", "女"), ("1", "男")
    )
    receiver_name = models.CharField(max_length=20, verbose_name='收货人姓名', null=True, blank=True)
    telephone_number = models.CharField(null=True, max_length=11, verbose_name='电话号码')
    city = models.CharField(max_length=30, verbose_name='城市', null=True, blank=True)
    address = models.CharField(max_length=70, verbose_name="详细地址", null=True, blank=True)
    gender = models.CharField(max_length=3, choices=gender_type, default="0", verbose_name="性别")
    register_date = models.DateField(auto_now_add=True, verbose_name='注册日期')
    receiver_id = models.IntegerField(default=None, verbose_name="默认的收货人ID")

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """邮箱验证"""
    send_type = (
        ("0", '注册'), ("1", '找回密码')
    )
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    send_type = models.CharField(max_length=5, choices=send_type, verbose_name='操作类型')
    send_date = models.DateTimeField(auto_now=True, verbose_name='发送的时间')

    class Meta:
        verbose_name = '邮箱验证'
        verbose_name_plural = verbose_name
        ordering = ('send_date',)

    def __str__(self):
        """返回发送的类型"""
        return self.get_send_type_display()


class Receiver(models.Model):
    user = models.ForeignKey('UserProfile', verbose_name='账户拥有着')
    name = models.CharField(max_length=20, verbose_name='收货人名字', null=True)
    city = models.CharField(max_length=30, verbose_name='城市', blank=True, null=True)
    address = models.CharField(max_length=70, null=True, verbose_name='详细地址')
    telephone = models.CharField(null=True, max_length=11, verbose_name='电话号码')

    class Meta:
        verbose_name = '收货人'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __str__(self):
        return self.name

