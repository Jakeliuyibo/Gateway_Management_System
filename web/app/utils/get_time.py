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
import logging

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

""" 获取当前日期 """
def get_current_date_apply_to_filename():
    return time.strftime('%Y_%m_%d', time.localtime(time.time()))

# """ 将日期格式转化为日期时间格式 """
# def transfer_format_from_date_to_datetime(date, type="start"):
#     date = datetime.datetime.strptime(date,"%Y-%m-%d")
#     if type == "start":     # format = "%Y-%m-%d 00:00:00"
#         return  date
#     elif type == "end":     # format = "%Y-%m-%d 23:59:59"
#         return  date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

'''
description: 将日期时间格式转化为日期格式
input  "%Y-%m-%d %H:%M:%S"
return '%Y-%m-%d'
'''
def transfer_format_from_datetime_to_date(date_time):
    date = datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
    return date.strftime('%Y-%m-%d')

def transfer_format_from_datetime_to_date_H(date_time):
    date = datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
    return date.strftime('%Y-%m-%d %H')

def transfer_format_from_datetime_to_date_HM(date_time):
    date = datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
    return date.strftime('%Y-%m-%d %H:%M')

def transfer_format_from_datetime_to_date_HMS(date_time):
    date = datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
    return date.strftime('%Y-%m-%d %H:%M:%S')

'''
description: 将日期时间格式转化为日期格式
input  "%Y-%m-%d %H:%M:%S.%f"
return '%Y-%m-%d'
'''
def transfer_format_from_datetime_with_ms_to_date(date_time, ft):
    date = datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f")

    if ft == "D":
        return date.strftime('%Y-%m-%d')
    elif ft == "H":
        return date.strftime('%Y-%m-%d %H')
    elif ft == "M":
        return date.strftime('%Y-%m-%d %H:%M')
    elif ft == "S":
        return date.strftime('%Y-%m-%d %H:%M:%S')
    elif ft == "F":
        return date.strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
        logging.error("转换日期时间时传入格式出错")
        return None

'''
description: 将时间戳转化为日期时间
input  17012312313 or '17012312313'
return '%Y-%m-%d %H:%M:%S'
'''
def transfer_format_from_timestamp_to_datetime(time_stamp : int):
    dt_object = datetime.datetime.fromtimestamp(time_stamp)
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

'''
description: 计算两个日期时间差值
input  '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S', threshold(unit : miniutes)
return {int} 相差的时间(unit: 秒)
'''
def cal_difftime_between_datetime(start_datetime, end_datetime):
    start_time  = datetime.datetime.strptime(start_datetime,"%Y-%m-%d %H:%M:%S")
    end_time    = datetime.datetime.strptime(end_datetime  ,"%Y-%m-%d %H:%M:%S")
    return (end_time - start_time).total_seconds()


""" 根据起始日期时间生成日期区间 """
def generate_dateinterval_by_datetime(start_datetime, end_datetime, format):
    # str格式转化为datetime
    if format   == "D":
        ft       = '%Y-%m-%d'
        ft_brief = '%m-%d'
        it = datetime.timedelta(days=1)
    elif format == "H":
        ft = '%Y-%m-%d %H'
        ft_brief = '%m-%d %H'
        it = datetime.timedelta(hours=1)
    elif format == "M":
        ft = '%Y-%m-%d %H:%M'
        ft_brief = '%H:%M'
        it = datetime.timedelta(minutes=1)
    elif format == "S":
        ft = '%Y-%m-%d %H:%M:%S'
        ft_brief = '%H:%M:%S'
        it = datetime.timedelta(seconds=1)
    else:
        logging.error("生成区间时格式异常")
        return

    st = datetime.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
    et = datetime.datetime.strptime(end_datetime  , '%Y-%m-%d %H:%M:%S')

    # 生成区间
    date_list = []
    date_brief_list = []
    while st < et:
        # 日期转字符串存入列表
        date_list.append(st.strftime(ft))
        date_brief_list.append(st.strftime(ft_brief))

        # 日期叠加
        st = st + it

    return date_list, date_brief_list

