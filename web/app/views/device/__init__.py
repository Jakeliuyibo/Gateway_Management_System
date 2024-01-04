# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved 
Author: liuyibo 1299502716@qq.com
Date: 2023-01-10 22:07:08
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-10 22:07:15
FilePath: \Gateway_Management_System\app\views\device\__init__.py
Description: 
'''
from flask import Blueprint

# 项目版本
PROJECT_VERSION = "V1.1"

# HTML 网页路径
TEMPLATEs_PATH  = "templates/"
HTML_PATH       = "device/"

# 创建蓝图，管理多个函数视图
device_blue = Blueprint("device", __name__, template_folder=TEMPLATEs_PATH + HTML_PATH, url_prefix='/device')
from . import views