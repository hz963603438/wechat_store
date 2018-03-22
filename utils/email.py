#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-08 21:43:43
# @Author  : kevin (wuhao@idvert.com)
# @Link    : http://idvert.com/

from account.models import EmailVerifyRecord

from django.core.mail import send_mail as django_send_mail
from django.conf import settings

import string
import random
import hashlib

def random_str():
    """生成8位验证码"""
    str = ''
    chars = string.ascii_letters + string.digits
    length = len(chars) - 1
    ran = random.Random()
    for i in range(8):
        str += chars[ran.randint(0, length)]
    m = hashlib.md5() # 采用md5 加密
    m.update(str)
    ret = m.hexdigest() # 进行加密 不把加完密的字符串存入到数据库
        # 进行验证的时候 取出进行验证
    return str


def send_email(email, send_type=0):
	"""
		发送邮件
		@email 邮件发送人
		@send_type 0为注册激活, 1为忘记密码
	"""

	email_record = EmailVerifyRecord()
	random_code = random_str()

	email_record.email=email
	email_record.code = random_code
	email_record.send_type = send_type
	email_record.save()



	if send_type == 0:
		eamil_title = u"欢迎注册"
		a_href = u"{0}/account/active/{1}".format(settings.LOCALHOST, random_code)
		eamil_body = u"<a href='{0}'>欢迎注册 请点击下面的连接进行激活</a>".format(a_href)
	elif send_type == 1:
		eamil_title = u"忘记密码"
		a_href = u"{0}/account/modify_password/{1}".format(settings.LOCALHOST, random_code)
		eamil_body = u"<a href='{0}'>请点击下面的链接修改密码</a>".format(a_href)

	status = django_send_mail(eamil_title, '', settings.EMAIL_FROM, [email], html_message=eamil_body)
	print status
	return status