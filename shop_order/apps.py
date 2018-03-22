# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ShopOrderConfig(AppConfig):
    name = 'shop_order'

    def ready(self):
        import signals

