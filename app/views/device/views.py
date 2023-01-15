# -*- coding: utf-8 -*-
'''
Author: liuyibo 1299502716@qq.com
Date: 2023-01-10 22:08:05
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-01-15 16:52:50
FilePath: \Gateway_Management_System\app\views\device\views.py
Description: 注册device模块的view视图
'''
import logging

from app.public import amis_ret
from app.utils.get_time import get_current_time

from . import *
from flask import current_app, jsonify, render_template, request, make_response, redirect, url_for, session, json
from app import db, redis_store
from app.models.models import User, Device
from sqlalchemy.sql import and_


def check_login_status():
    """ check login cookie from session """
    login_flag = session.get("login_flag")
    user_name  = session.get("user_name")

    if login_flag == "success" and user_name:
        return True
    else:
        return False


@device_blue.route("/")
@device_blue.route("/index", methods=['GET'])
def index():
    """ 设备首页操作：校验cookie并查询数据库中用户信息   """
    if check_login_status():
        return render_template(HTML_PATH + "index.html")
    else:
        return redirect("/login/index")


@device_blue.route('/data_operation', methods=['GET'])
def get_devices_info():
    """ 获取数据库设备信息  """
    requst_args   = request.args
    # perPage  = int(requst_args.get('perPage'))
    # page     = int(requst_args.get('page'))
    # keywords = request.values.get('keywords')
    orderBy  = requst_args.get('orderBy')
    orderDir = requst_args.get('orderDir')
    search_device_id    = request.values.get('device_id')
    search_device_name  = request.values.get('device_name')
    try:
        # 条件模糊查询
        db_obj = db.session.query(Device).filter(
            Device.device_id.like(f'%{search_device_id}%' if search_device_id else '%%'),
            Device.device_name.like(f'%{search_device_name}%' if search_device_name else '%%'))

        if orderBy and orderDir:
            # 排序
            order = getattr(Device, orderBy)        # equal: Device.device_id
            order = getattr(order, orderDir)()      # equal: order=order.asc()
            db_obj = db_obj.order_by(order)

        # 查询数据库中所有设备信息
        devices = db_obj.all()
        devices_count = db_obj.count()
        device_list = [dev.to_dict() for dev in devices]

        ret_data = {
            "device_count"  : devices_count,
            "device_list"   : device_list,
        }
        return amis_ret(data=ret_data, status=0, msg="查询设备信息成功")
    except Exception as e:
        logging_msg = "SQL Error: try to get device info" + str(e)
        logging.error(logging_msg)
        return amis_ret(data={}, status=-1, msg="查询设备信息失败")

@device_blue.route('/data_operation/<int:device_id>', methods=['PUT'])
def modify_device_info(device_id):
    """ 修改数据库设备信息  """
    requst_body = request.get_data()            
    try:
        modify_device = db.session.query(Device).filter_by(device_id=device_id).first()
        if modify_device:
            # requst_args = json.loads(modify_device.to_dict())
            # requst_args = json.loads(json.dumps(modify_device.to_dict(),ensure_ascii=False))
            
            # modify device info
            requst_args = json.loads(requst_body)
            requst_args['last_edit_time'] = get_current_time()
            modify_device.modify_from_dict(requst_args)

            db.session.commit()
            return amis_ret(data={}, status=0, msg="修改设备成功")
        else:
            raise
    except Exception as e:
        logging_msg = "SQL Error: try to modify device=" + str(device_id) + str(e)
        logging.error(logging_msg)
        return amis_ret(data={}, status=-1, msg="修改设备失败")

@device_blue.route('/data_operation/<int:device_id>', methods=['DELETE'])
def delete_device_info(device_id):
    """ 删除数据库设备信息  """
    try:
        db.session.query(Device).filter_by(device_id=device_id).delete()
        db.session.commit()
        return amis_ret(data={}, status=0, msg="删除设备成功")
    except Exception as e:
        logging_msg = "SQL Error: try to delete device=" + str(device_id) + str(e)
        logging.error(logging_msg)
        return amis_ret(data={}, status=-1, msg="删除设备失败")

@device_blue.route("/logout", methods=['GET'])
def logout():
    """ 登出操作：删除cookie并转到登陆界面   """
    ret_data = {}
    if check_login_status():
        ret_data['user_name'] = session.get("user_name")

        # clear cookie
        session.clear()
        return amis_ret(data=ret_data,status=0,msg="退出登录成功",errors={})
    else:
        return redirect("/login/index")
