'''
Author: liuyibo 1299502716@qq.com
Date: 2023-01-07 12:47:25
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-07 22:18:51
FilePath: \Gateway_Management_System\app\__init__.py
Description: app文件夹自动初始化文件，创建Flask对象
'''
from app.config import config_dict
import logging
from redis import StrictRedis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# 声明全局变量
db = None               # 创建数据库ROM变量
redis_store = None      # 创建redis变量

def create_app(config_name):
    # create flask object
    app = Flask(__name__)

    # 配置Flask对象
    config_obj = config_dict.get(config_name)
    app.config.from_object(config_obj)

    # 关联数据库ROM和Flask对象
    global db
    db = SQLAlchemy()
    db.init_app(app)

    # 初始化redis对象，并从config获取redis配置
    global redis_store
    redis_store = StrictRedis(host=config_obj.REDIS_HOST, port=config_obj.REDIS_PORT)

    # 创建session对象
    Session(app)

    # 关联注册蓝图与Flask对象
    from app.views.login  import login_blue
    app.register_blueprint(login_blue , url_prefix="")       # register login blue

    return app