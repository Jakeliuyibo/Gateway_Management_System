# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved 
Author: liuyibo 1299502716@qq.com
Date: 2023-01-07 12:47:25
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-14 22:29:33
FilePath: \Gateway_Management_System\app\__init__.py
Description: app文件夹自动初始化文件，创建Flask对象
'''
from app.config import config_dict
import logging
from redis import StrictRedis
from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# 声明全局变量
db          = SQLAlchemy()      # 创建数据库ROM变量
redis_store = None              # 创建redis变量

def create_app(config_name):
    # create flask object
    app = Flask(__name__)

    # 配置Flask对象
    config_obj = config_dict.get(config_name)
    app.config.from_object(config_obj)

    # init logging and binding app's handler
    if config_obj.LOGGING_CONFIG_ABLE:
        logs_init(app, config_obj)

    # 关联数据库ROM和Flask对象
    db.init_app(app)

    # 初始化redis对象，并从config获取redis配置
    global redis_store
    redis_store = StrictRedis(host=config_obj.REDIS_HOST, port=config_obj.REDIS_PORT)

    # 创建session对象
    Session(app)

    # 关联index、login、device蓝图与Flask对象
    from app.views.index  import index_blue
    from app.views.login  import login_blue
    from app.views.device import device_blue

    app.register_blueprint(index_blue)          # register index blue
    app.register_blueprint(login_blue)          # register login blue
    app.register_blueprint(device_blue)         # register device blue

    return app

'''
description: init logging module
return {*}
'''
def logs_init(binding_app, config):
    
    # 创建logging对象
    mlogger = logging.getLogger()
    mlogger.setLevel(logging.DEBUG)

    # 配置logging文件路径与终端路径
    file_handler = logging.FileHandler(config.LOGGING_FILE_PATH, mode='a', encoding="utf-8")
    stream_handler = logging.StreamHandler()
    # file_handler = logging.handlers.RotatingFileHandler("test.log", mode="w", maxBytes=1000, backupCount=3, encoding="utf-8")# 每隔 1000 Byte 划分一个日志文件，备份文件为 3 个
    # handler2 = logging.handlers.TimedRotatingFileHandler("test.log", when="H", interval=1, backupCount=10)# 每隔 1小时 划分一个日志文件，interval 是时间间隔，备份文件为 10 个

    # 配置logging等级与格式
    file_handler.setLevel(config.LOGGING_FILE_HANDLER_LEVEL)
    stream_handler.setLevel(config.LOGGING_STREAM_HANDLER_LEVEL)
    file_handler.setFormatter(config.LOGGING_FILE_FORMAT)
    stream_handler.setFormatter(config.LOGGING_STREAM_FORMAT)

    # 为flask的日志记录器中添加handler
    mlogger.addHandler(file_handler)
    mlogger.addHandler(stream_handler)
    binding_app.logger.addHandler(mlogger)


