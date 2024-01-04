"""
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved
Author: liuyibo 1299502716@qq.com
Date: 2023-01-14 23:06:18
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-02-24 10:33:07
FilePath: /Gateway_Management_System/app/utils/get_time.py
Description: 时间相关函数
"""
import datetime
import time
import datedays

""" 获取当前时间 """
def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

""" 获取当前时间，带有小数 """
def get_current_time_with_ms():
    dt = datetime.datetime.fromtimestamp(time.time())
    return dt.strftime('%Y-%m-%d %H:%M:%S.%f')

""" 获取当前时间 """
def get_current_time_apply_to_filename():
    return time.strftime('%Y_%m_%d %H_%M_%S', time.localtime(time.time()))

def transfer_format_from_date_to_datetime(date, type="start"):
    """ 将日期格式转化为日期时间格式 """
    date = datetime.datetime.strptime(date,"%Y-%m-%d")
    if type == "start":     # format = "%Y-%m-%d 00:00:00"
        return  date
    elif type == "end":     # format = "%Y-%m-%d 23:59:59"
        return  date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

def transfer_format_from_datetime_to_date(date_time):
    """ 将日期时间格式转化为日期格式 """
    date = datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
    return date.strftime('%Y-%m-%d')

def transfer_format_from_datetime_with_ms_to_date(date_time):
    """ 将日期时间格式转化为日期格式 """
    date = datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f")
    return date.strftime('%Y-%m-%d')

def generate_datelist_by_startenddate(start_date, end_date):
    """ 根据起始日期生成器件的日期列表 """
    # str格式转化为datetime
    start_date  = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date    = datetime.datetime.strptime(end_date,'%Y-%m-%d')

    date_list = []
    date_list.append(start_date.strftime('%Y-%m-%d'))
    while start_date < end_date:
        # 日期叠加一天
        start_date = start_date + datetime.timedelta(days=1)
        # 日期转字符串存入列表
        date_list.append(start_date.strftime('%Y-%m-%d'))
    return date_list