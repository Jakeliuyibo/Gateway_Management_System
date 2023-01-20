# -*- coding: utf-8 -*-
'''
Author: liuyibo 1299502716@qq.com
Date: 2023-01-07 12:47:25
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-20 15:17:01
FilePath: \Gateway_Management_System\app\views\login\views.py
Description: 注册login模块的view视图
'''

import logging
from . import *
from flask import current_app, jsonify, render_template, request, make_response, redirect, url_for, session
from app import db, redis_store
from app.models.models import User, Device
from sqlalchemy.sql import and_
from app.config import Config

@login_blue.route("/")
@login_blue.route("/index")
def index():
    """ 登陆操作：从URL中获得login.html输入的用户名和密码，校验数据库并设置cookie   """
    ret = request.args
    if ret:
        rqu_user_name = ret.get("Username")
        rqu_password = ret.get("Password")

        # 查询数据库中用户数据
        try:
            db.session.query(User).filter(and_(User.user_name == rqu_user_name, User.user_password == rqu_password)).one()
        except:
            # 设置cookie，有效期 3600 sec
            session['login_flag'] = "fail"
        else:
            session['login_flag'] = "success"
            session['user_name']  = rqu_user_name

        # 设置响应，引导至profile界面
        return redirect("/device/index")
    else:
        return render_template(HTML_PATH + "login.html", version=Config.PROJECT_VERSION)
