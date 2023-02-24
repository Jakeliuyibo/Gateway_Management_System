# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved 
Author: liuyibo 1299502716@qq.com
Date: 2023-01-11 17:53:54
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-11 18:07:01
FilePath: \Gateway_Management_System\app\views\index\views.py
Description: 注册index模块的view视图
'''


from . import *
from flask import redirect, session

@index_blue.route("/test")
def test():
    return "test"


@index_blue.route("/")
@index_blue.route("/index")
def index():
    """ 首页引导操作：根据session判断用户是否登录，选择引导界面   """
    try:
        # 尝试获取login_flag
        login_flag = session.get("login_flag")
        if login_flag == "success":
            # 已登录，跳转至device界面
            return redirect("device/index")
        else:
            raise
    except:
            # 未登录，跳转至login界面
            return redirect("login/index")
