'''
Author: TheDraco
Date: 2022-12-12 15:10:59
LastEditTime: 2023-01-05 17:45:23
Description:
FilePath: /10_flask/app/__init__.py
'''
from datetime import timedelta
import os
from redis import StrictRedis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# create flask object
app = Flask(__name__)

class Config(object):
    # 调试模式
    DEBUG = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getcwd() + "/app/db/users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置，保存数据库地址、端口、session信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session配置
    SECRET_KEY = os.urandom(24)                                     # 设置session密钥
    SESSION_TYPE = "redis"                                          # 设置session存储类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)   # 设置session redis服务器地址
    SESSION_USE_SIGNER = True                                       # 设置签名
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)                 # 设置session有效期one hour

# 配置app
app.config.from_object(Config)

# 创建数据库ROM对象, 并关联Flask对象
db = SQLAlchemy()
db.init_app(app)

# 创建redis对象，并从Config获取redis配置
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 创建session对象
Session(app)

from app.views.views  import user_blue
app.register_blueprint(user_blue , url_prefix="")       # register user blue