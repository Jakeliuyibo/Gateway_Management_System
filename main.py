# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved 
Author: liuyibo 1299502716@qq.com 
Date: 2023-01-07 12:47:25
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-02-24 10:25:20
FilePath: \Gateway_Management_System\main.py
Description: 主函数
'''

from app import create_app

if __name__ == "__main__":
    # create flask app
    web_app = create_app("develop")
    
    # execute app
    web_app.run(host="localhost", port="1234")