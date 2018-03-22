from django.dispatch import receiver
from django.db.models.signals import pre_save

from django.db.models import F

from .models import OrderMain, OrderDetail
from django.db import transaction

@receiver(pre_save, sender=OrderMain)
@transaction.atomic
def order_save(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.is_pay == "-1":
        orderDetails = OrderDetail.objects.filter(order=instance).all()
        for od in orderDetails:
            od.goods_info.stock = F("stock") + od.count
            od.save()








