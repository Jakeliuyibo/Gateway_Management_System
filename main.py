# -*- coding: utf-8 -*-
'''
Author: liuyibo 1299502716@qq.com
Date: 2023-04-29 21:35:29
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-06-26 19:52:36
FilePath: \Gateway_System\main.py
Description: 主函数，通过python main.py启动网关软件
'''
# 为了防止Linux使用sudo python main.py执行程序时与python main.py的调用包不同，因此添加路径
import platform
# if platform.system() == 'Linux':
#     import sys
#     sys.path.insert(0, r"/home/nano/.local/lib/python3.8/site-packages")
from multiprocessing import Process
from web.app import create_app, run_test_server

'''
description: 进程：运行网关设备管理APP
'''
def create_web():
    # create flask app
    web_app = create_app("develop")

    # # execute app
    run_test_server(web_app)

if __name__ == "__main__":

    # 创建测试web服务器进程
    proc_web = Process(target=create_web, args=())
    proc_web.start()
    proc_web.join()