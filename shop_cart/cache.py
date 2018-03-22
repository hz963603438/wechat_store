# -*- coding: utf-8 -*-

from utils.redis import conn


class CartCache(object):

    def __init__(self, user):
        self.user_browse_cache_key = "cart_user_{0}".format(user.id)


    def add_cart(self, goods_id, goods_count):
        conn.hset(self.user_browse_cache_key, goods_id, goods_count)


    def get_all(self):
        return conn.hgetall(self.user_browse_cache_key)

    def del_cart(self, goods_id):
        return conn.hdel(self.user_browse_cache_key, str(goods_id))

    def update_cart(self, goods_id, oper, buy_num=None):
        assert oper in ["+", "-", "custom"]

        with conn.pipeline() as pipe:
            pipe.multi()
            if oper == "custom":
                _buy_num = buy_num
            else:
                _buy_num = int(conn.hget(self.user_browse_cache_key, goods_id))
                _buy_num = _buy_num + 1 if oper == "+" else _buy_num - 1

            if _buy_num <= 0:
                pipe.hdel(self.user_browse_cache_key, goods_id)
            else:
                pipe.hset(self.user_browse_cache_key, goods_id, _buy_num)
            pipe.execute()

    def get_one(self, gid):
        return conn.hget(self.user_browse_cache_key, gid)


