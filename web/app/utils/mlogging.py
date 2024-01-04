# -*- coding: utf-8 -*-
'''
Author: liuyibo 1299502716@qq.com
Date: 2023-02-15 16:34:27
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-02-15 17:09:49
FilePath: /RL_Simulation_Of_UWSNs/utils/mlogging.py
Description: 调试打印配置
'''
import logging

'''
description: init logging module, debug << info << warning << error << critical
'''
def logs_init(config):
    # 创建logging对象
    mlogger = logging.getLogger()
    mlogger.setLevel(logging.DEBUG)

    # 配置logging 终端输出和文件输出的路径、等级、格式
    fh = logging.FileHandler(config.LOGGING_FILE_PATH, mode='a', encoding="utf-8")
    fh.setLevel(config.LOGGING_FILE_HANDLER_LEVEL)

    ch = logging.StreamHandler()
    ch.setLevel(config.LOGGING_STREAM_HANDLER_LEVEL)
    
    # formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    fh.setFormatter(config.LOGGING_FILE_FORMAT)
    ch.setFormatter(config.LOGGING_STREAM_FORMAT)

    # 为日志记录器中添加handler
    mlogger.addHandler(fh)
    mlogger.addHandler(ch)

    return mlogger