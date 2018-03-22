# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from django.db.models import Q
from django.http import JsonResponse, HttpResponse

from shop.models import GoodsInfo
from shop.cache import BrowseCache
from .models import UserProfile, EmailVerifyRecord, Receiver
from .form import RegisterForm
from shop_order.models import OrderMain, OrderDetail

from utils.email import send_email

from django.contrib.auth.decorators import login_required

# Create your views here.

def check_username(request):
    username = request.GET.get("username")
    count = UserProfile.objects.filter(username=username).count()
    return JsonResponse({"count": count})


def send_email_success(request):
    return render(request, "account/send_success.html")


def send_email_test(request):
    send_email("343446040@qq.com", send_type=1)
    return render(request, "account/send_success.html")


class RegisterView(View):

    def get(self, request):
        return render(request, "account/register.html")

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            response = self.save_user(request)
        return response

    def save_user(self, request):
        username = request.POST.get("username")
        passwd1 = request.POST.get("password1")
        passwd2 = request.POST.get("password2")
        email = request.POST.get("email")
        allow = request.POST.get("allow")

        if allow != "1":
            err_allow = u"请阅读并同意我们的协议"
            return render(request, "account/register.html", locals())

        if passwd1 != passwd2:
            err = u"两次密码不一致"
            return render(request, "account/register.html", locals())

        user = UserProfile.objects.filter(
            Q(username=username) | Q(email=email)).first()

        if user:
            err = u"用户已经存在"
            return render(request, "account/register.html", locals())

        user = UserProfile()
        user.username = username
        user.password = make_password(passwd1)
        user.email = email
        user.is_active = False
        user.save()

        send_email(email, send_type=0)
        return redirect("/account/send_email_success/")


class ActiveView(View):

    def get(self, request, active_code):
        email_record = EmailVerifyRecord.objects.filter(
            code=active_code).first()

        if not email_record:
            return JsonResponse({"message": u"注册码错误"})

        else:
            user = UserProfile.objects.filter(email=email_record.email).first()
            user.is_active = True
            user.save()
            return redirect("/account/login/")


class LoginView(View):

    def get(self, request):
        return render(request, "account/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('/shop/index/')
        else:
            err = u"用户名或密码错误"
            return render(request, "account/login.html", locals())


class ModifyView(View):

    def get(self, request):
        return render(request, "account/forget_password.html")

    def post(self, request):
        email = request.POST.get("email")

        user = UserProfile.objects.filter(email=email).count()
        if user:
            send_email(email, send_type=1)
            message = u"成功发送邮件"
        else:
            message = u"用户名不存在"
        print message
        return render(request, "account/forget_password.html", locals())


class ModifyPasswordView(View):

    def get(self, request, reset_code):
        email_record = EmailVerifyRecord.objects.filter(
            code=reset_code).first()
        if email_record:
            email = email_record.email
            return render(request, "account/reset_password.html", locals())
        else:
            return JsonResponse({"messge": u"错误"})

    def post(self, request, reset_code):
        passwd1 = request.POST.get("password1")
        passwd2 = request.POST.get("password2")
        email = request.POST.get("email")

        if len(passwd1) < 8 and passwd1 != passwd2:
            err = u"密码设置错误"
            return render(request, "account/reset_password.html", locals())

        user = UserProfile.objects.filter(email=email).first()
        if not user:
            err = u"用户名不存在"
            return render(request, "account/reset_password.html", locals())
        else:
            password = make_password(passwd1)
            user.password = password
            user.save()
            return redirect("/account/home/")

def logout_view(request):
    logout(request)
    return redirect("/shop/index/")


@login_required
def user_center_info(request):
    browses = BrowseCache.get_browse(request.user)
    goods_info = GoodsInfo.objects.filter(id__in=browses)
    return render(request, "account/user_center_info.html", locals())


@login_required
def user_center_site(request):
    if request.method == "POST":
        username = request.POST.get("username")
        city = request.POST.get("city")
        telephone = request.POST.get("telephone")
        address = request.POST.get("address")

        receiver = Receiver()
        receiver.user = request.user
        receiver.name = username
        receiver.address = address
        receiver.telephone = telephone
        receiver.city = city
        receiver.save()

        return redirect("/account/user_center_site/")
    elif request.method == "GET":
        receiver_infos = Receiver.objects.filter(user=request.user).all()

    return render(request, "account/user_center_site.html", locals())


@login_required
def user_center_set_default_site(request):
    data_id = request.GET.get("data_id")
    receiver = Receiver.objects.get(pk=data_id)

    request.user.receiver_name = receiver.name
    request.user.telephone_number = receiver.telephone
    request.user.city = receiver.city
    request.user.address = receiver.address
    request.user.receiver_id = receiver.id
    request.user.save()
    return JsonResponse({"telephone": receiver.telephone,
                         "address": receiver.address,
                         "name": receiver.name})

 
@login_required
def user_center_del_default_site(request):
    data_id = request.GET.get("data_id")

    Receiver.objects.filter(id=data_id).delete()
    if request.user.receiver_id == int(data_id):
        request.user.receiver_name = None
        request.user.telephone_number = None
        request.user.city = None
        request.user.address = None
        request.user.receiver_id = 0
        request.user.save()

    return JsonResponse({"status": 0})


@login_required
def user_center_order(request):
    curr_page = int(request.GET.get("curr_page", 1))
    order_info = []

    orders = OrderMain.objects.filter(user=request.user).exclude(is_pay__in=["0"])
    p = Paginator(orders, 3)
    page = p.page(curr_page)

    # 要分页后才查询
    for obj in page.object_list:
        order_info.append({
            "order": obj,
            "order_details": OrderDetail.objects.filter(order=obj).all()
        })


    return render(request, "account/user_center_order.html", locals())