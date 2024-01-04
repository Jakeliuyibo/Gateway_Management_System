# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved
Author: liuyibo 1299502716@qq.com
Date: 2023-01-07 20:32:38
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-20 15:16:19
FilePath: \Gateway_Management_System\app\views\login\__init__.py
Description:
'''
from flask import Blueprint


# HTML 网页路径
TEMPLATEs_PATH  = "templates/"
HTML_PATH       = "login/"

# 创建蓝图，管理多个函数视图
login_blue = Blueprint("login", __name__, template_folder=TEMPLATEs_PATH + HTML_PATH, url_prefix='/login')
from . import views