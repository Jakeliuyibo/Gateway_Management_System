'''
Author: TheDraco
Date: 2022-12-12 15:10:59
LastEditTime: 2023-01-05 17:45:23
Description:
FilePath: /10_flask/app/__init__.py
'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create flask object
app = Flask(__name__)

class app_config(object):
    # 调试模式
    DEBUG = True

    # session配置
    SECRET_KEY = os.urandom(24)

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getcwd() + "/app/db/users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(app_config)

# 创建数据库ROM对象, 并关联Flask对象
db = SQLAlchemy()
db.init_app(app)

# register user blue
from app.views.views  import user_blue
app.register_blueprint(user_blue , url_prefix="")