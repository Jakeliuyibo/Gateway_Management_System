# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved 
Author: liuyibo 1299502716@qq.com
Date: 2023-01-07 12:47:25
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-05-03 16:16:32
FilePath: \Gateway_Management_System\app\__init__.py
Description: app文件夹自动初始化文件，创建Flask对象
'''
from .utils.mlogging import logs_init
from .config import Config, config_dict
from redis import StrictRedis
from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import logging
import pika

# 声明全局变量
app         = Flask(__name__)   # flask object
db          = SQLAlchemy()      # 创建数据库ROM变量
redis_store = None              # 创建redis变量

# 初始化pika
pika_credentials = pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD)
pika_connection  = pika.BlockingConnection(pika.ConnectionParameters(Config.RABBITMQ_HOSTNAME, Config.RABBITMQ_PORT, '/', pika_credentials, heartbeat=0))
pika_channel     = pika_connection.channel()

'''
description: 创建Flask APP
'''
def create_app(config_name):

    # 配置Flask对象
    config_obj = config_dict.get(config_name)
    app.config.from_object(config_obj)

    # init logging and binding app's handler
    if config_obj.LOGGING_CONFIG_ABLE:
        mloger = logs_init(config_obj)
        app.logger.addHandler(mloger)

    logging.critical(f"数据库地址{config_obj.SQLALCHEMY_DATABASE_URI}")

    # 关联数据库ROM和Flask对象
    global db
    db.init_app(app)

    # 初始化redis对象，并从config获取redis配置
    global redis_store
    redis_store = StrictRedis(host=config_obj.REDIS_HOST, port=config_obj.REDIS_PORT)

    # 创建session对象
    Session(app)

    # 关联index、login、device蓝图与Flask对象
    from .views.index  import index_blue
    from .views.login  import login_blue
    from .views.device import device_blue

    app.register_blueprint(index_blue)          # register index blue
    app.register_blueprint(login_blue)          # register login blue
    app.register_blueprint(device_blue)         # register device blue

    return app

'''
description: 运行测试APP
'''
def run_test_server(app):
    # execute app
    app.run(host="localhost", port="19999", debug=False)