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

# SQLITE 数据库路径和URL
SQLITE_DB_ABSOULTE_PATH = os.getcwd() + "/app/db/users.db"
SQLITE_DB_URL = "sqlite:///" + SQLITE_DB_ABSOULTE_PATH
print(SQLITE_DB_URL)

# 创建数据库ROM对象
db = SQLAlchemy()

def create_app():
    # create flask object
    app = Flask(__name__)

    # 使用session密钥
    app.config['SECRET_KEY'] = os.urandom(24)
    # 设置数据库的链接地址
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLITE_DB_URL
    # 关闭追踪数据库的修改
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # register admin blue
    from app.views.views  import user1_blue
    app.register_blueprint(user1_blue , url_prefix="")

    # 关联数据库与Flask对象
    db.init_app(app)

    return app