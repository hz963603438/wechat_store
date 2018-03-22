# -*- coding: utf-8 -*-

from utils.redis import conn


class BrowseCache(object):
    user_browse_cache_key = "user_browse_cache_key_{0}"

    @classmethod
    def set_browse(cls, user, gid):
        conn.zadd(cls.user_browse_cache_key.format(user.id), str(1), gid)

    @classmethod
    def get_browse(cls, user, start=-10, end=-1):
        return conn.zrange(cls.user_browse_cache_key.format(user.id), start, end)

