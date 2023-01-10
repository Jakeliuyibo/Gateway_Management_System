# -*- coding: utf-8 -*-
'''
Author: liuyibo 1299502716@qq.com
Date: 2023-01-07 12:47:25
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-10 14:40:07
FilePath: \Gateway_Management_System\app\views\login\views.py
Description: 注册login模块的view视图
'''

import logging
from . import *
from flask import render_template, request, make_response, redirect, url_for, session
from app import db, redis_store
from app.models.models import User
from sqlalchemy.sql import and_

@login_blue.route("/")
def test():
    redis_store.set("name","test")
    # logging.debug(redis_store.get("name"))
    logging.debug("debug")
    logging.info("info")
    logging.error("ERROR")
    return "test"

@login_blue.route("/login")
def login():
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
            # response.set_cookie("login_flag", "fail"   , max_age=3600)
            session['login_flag'] = "fail"
        else:
            # response.set_cookie("login_flag", "success", max_age=3600)
            session['login_flag'] = "success"
            session['user_name']  = rqu_user_name

        # 设置响应，引导至profile界面
        return make_response(redirect("profile"))
    else:
        return render_template(HTML_PATH + "login.html", version=PROJECT_VERSION)

@login_blue.route("/profile")
def profile():
    """ 简历操作：校验cookie并查询数据库中用户信息   """
    # check cookie
    login_flag = session.get("login_flag")
    user_name  = session.get("user_name")

    if login_flag == "success" and user_name:

        # 查询数据库中用户数据
        obj = db.session.query(User).filter(User.user_name == user_name).one()

        # 模板渲染
        return render_template(HTML_PATH + "profile.html", user_name=obj.user_name, user_profile=obj.user_profile)
    else:
        return redirect("login")

@login_blue.route("/logout")
def logout():
    """ 登出操作：删除cookie并转到登陆界面   """
    session.clear()
    return redirect("login")
