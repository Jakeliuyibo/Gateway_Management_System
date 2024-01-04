# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved 
Author: liuyibo 1299502716@qq.com
Date: 2023-01-11 17:53:12
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-11 17:55:45
FilePath: \Gateway_Management_System\app\views\index\__init__.py
Description: 
'''
from flask import Blueprint


# 创建蓝图，管理多个函数视图
index_blue = Blueprint("index", __name__, url_prefix='')
from . import views