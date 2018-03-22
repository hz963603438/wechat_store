# -*- coding: utf-8 -*-

from django_redis import get_redis_connection

__all__ = ["conn"]

conn = get_redis_connection("default")