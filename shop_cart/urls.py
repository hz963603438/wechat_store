"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from shop_cart import views

urlpatterns = [
    url(r'^shop_cart/$', views.shop_cart, name="shop_cart"),
    url(r'^add_cart/(?P<gid>\d*)/$', views.add_cart, name="add_cart"),
    url(r'^del_cart/(?P<gid>\d*)/', views.del_cart, name="del_cart"),
    url(r'^update_cart/(?P<gid>\d*)/', views.update_cart, name="update_cart"),
]
