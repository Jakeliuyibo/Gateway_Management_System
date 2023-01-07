'''
Author: liuyibo 1299502716@qq.com
Date: 2023-01-07 12:47:25
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-07 21:43:36
FilePath: \Gateway_Management_System\main.py
Description: 主函数
'''
from app import create_app


if __name__ == "__main__":
    app = create_app("develop")

    # execute app
    app.run(host="localhost", port="1234")