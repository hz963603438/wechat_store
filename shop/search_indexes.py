# -*- coding: utf-8 -*-
from haystack import indexes
from shop.models import GoodsInfo


# 这个class的命名必须要Model的类名+Index
class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    # 固定为该值，所有定义的属性中，只能有一个document=True
    text = indexes.CharField(document=True, use_template=True)

    # 关联的Model
    def get_model(self):
        return GoodsInfo

    # 添加或者更新索引时需要查询的数据
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()