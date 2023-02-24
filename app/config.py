# -*- coding: utf-8 -*-
'''
Author: liuyibo 1299502716@qq.com
Date: 2023-01-07 19:06:57
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-02-24 10:10:02
FilePath: \Gateway_Management_System\app\config.py
Description: flask的默认配置
'''
import os
import logging
from datetime import timedelta
from redis import StrictRedis

'''
description: 基础配置类
'''
class Config(object):
    # 调试模式配置
    DEBUG = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getcwd() + "/app/db/gateway.db"
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

    # logging配置
    LOGGING_CONFIG_ABLE          = False
    LOGGING_FILE_PATH            = 'logs/log'                       # 设置logging文件输出路径
    LOGGING_FILE_HANDLER_LEVEL   = logging.WARNING                  # 设置logging文件输出等级
    LOGGING_STREAM_HANDLER_LEVEL = logging.DEBUG                    # 设置logging终端输出等级
    LOGGING_FILE_FORMAT          = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    LOGGING_STREAM_FORMAT        = logging.Formatter('%(message)s')
    
    # upload文件上传配置
    UPLOAD_FILE_STORAGE_PATH     = "storage/upload"                 # 设置上传文件存储路径

    # 项目版本
    PROJECT_VERSION              = "V1.1"
'''
description: 开发配置
'''
class DevelopConfig(Config):
    # 调试模式配置
    DEBUG = True
'''
description: 生产配置
'''
class ProductConfig(Config):
    # 调试模式配置
    DEBUG = False
    LOGGING_FILE_HANDLER_LEVEL   = logging.ERROR                    # 设置logging文件输出等级
    LOGGING_STREAM_HANDLER_LEVEL = logging.ERROR                    # 设置logging终端输出等级

config_dict = {
    "develop":  DevelopConfig,
    "product":  ProductConfig
}
