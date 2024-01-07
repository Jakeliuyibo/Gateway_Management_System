# -*- coding: utf-8 -*-
'''
Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved 
Author: liuyibo 1299502716@qq.com
Date: 2023-01-10 22:08:05
LastEditors: liuyibo 1299502716@qq.com
LastEditTime: 2023-06-26 21:05:54
FilePath: \Gateway_Management_System\app\views\device\views.py
Description: 注册device模块的view视图
'''
import os
import logging
import threading
import pika
from flask import current_app, jsonify, render_template, request, make_response, redirect, url_for, session, json
from . import *
from ... import db, redis_store, pika_channel_in, pika_channel_out, app
from ...public import amis_ret
from ...utils.get_time import *
from ...config import Config
from ...models.models import *
from ...models.event  import *
from sqlalchemy.sql import and_


# """"""""""""""""""""""""""""""""""   页面操作   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   页面操作   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   页面操作   """"""""""""""""""""""""""""""""""
""" 检测登录的用户状态 """
def check_login_status():
    login_flag = session.get("login_flag")
    user_name  = session.get("user_name")

    if login_flag == "success" and user_name:
        logging.critical(f"检测用户登录状态{user_name}成功")
        return True
    else:
        logging.error(f"检测用户登录状态{user_name}失败")
        return False

""" 设备首页操作：校验cookie并查询数据库中用户信息   """
@device_blue.route("/")
@device_blue.route("/index", methods=['GET'])
def get_index_html():
    if check_login_status():
        return render_template(HTML_PATH + "index.html", version=Config.PROJECT_VERSION)
    else:
        return redirect("/login/index")

""" 数据传输页面操作：校验cookie并查询数据库中用户信息   """
@device_blue.route("/data", methods=['GET'])
def get_data_html():
    if check_login_status():
        return render_template(HTML_PATH + "data.html", version=Config.PROJECT_VERSION)
    else:
        return redirect("/login/index")

""" 登出操作：删除cookie并转到登陆界面   """
@device_blue.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return amis_ret(data={}, status=0,msg="退出登录成功")

# """"""""""""""""""""""""""""""""""   数据操作：设备   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   数据操作：设备   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   数据操作：设备   """"""""""""""""""""""""""""""""""
""" 获取数据库设备信息  """
@device_blue.route('/data_operation', methods=['GET'])
def get_devices_info():
    requst_args         = request.args
    # perPage  = int(requst_args.get('perPage'))
    # page     = int(requst_args.get('page'))
    # keywords = request.values.get('keywords')
    orderBy             = requst_args.get('orderBy')
    orderDir            = requst_args.get('orderDir')
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
        logging.critical("查询数据库中设备信息成功")
        return amis_ret(data=ret_data, status=0, msg="查询设备信息成功")
    except Exception as e:
        logging.error(f"SQL Error: try to get device info, {e}")
        return amis_ret(data={}, status=-1, msg="查询设备信息失败")

""" 修改数据库设备信息  """
@device_blue.route('/data_operation/<int:device_id>', methods=['PUT'])
def modify_device_info(device_id):
    requst_body = request.get_data()
    try:
        modify_device = db.session.query(Device).filter_by(device_id=device_id).first()
        if modify_device:
            # requst_args = json.loads(modify_device.to_dict())
            # requst_args = json.loads(json.dumps(modify_device.to_dict(),ensure_ascii=False))

            # modify device info
            requst_args = json.loads(requst_body)
            requst_args['last_edit_time'] = get_current_time()

            # ! 检查是否打开或关闭模块
            if modify_device.device_status != requst_args["device_status"]:

                # 1、向数据库创建任务
                try:
                    sql_task                         = Tasks()
                    sql_task.priority                = 0
                    sql_task.submit_user             = session.get("user_name")
                    db.session.add(sql_task)
                    db.session.commit()

                    if requst_args['device_status'] == True:
                        sql_task.type                = Task_Type.DEVICE_OPEN.value
                    else:
                        sql_task.type                = Task_Type.DEVICE_CLOSE.value
                    sql_task.status                  = "schedule"     # success\pending\queue\schedule\fail
                    sql_task.submit_time             = get_current_time_with_ms()
                    sql_task.oper_device_id          = device_id 
                    sql_task.oper_device_name        = modify_device.device_name
                except Exception as e:
                    logging.error(f"创建设备({device_id})操作相关的任务错误， {e}")
                finally:
                    db.session.commit()

                # 2、通过pika向控制软件发送任务处理
                pika_channel_in.basic_publish(
                    exchange = Config.RABBITMQ_EXCHANGENAME_IN, routing_key = Config.RABBITMQ_ROUTINGKEY_IN, 
                    body = settle_device_event(sql_task.id, sql_task.type, device_id, ""))

            logging.critical(f"向数据库和控制软件申请修改设备{device_id}信息成功")
            return amis_ret(data={}, status=0, msg="成功提交修改，请刷新")
        else:
            raise
    except Exception as e:
        logging.error(f"尝试提交修改设备{device_id}信息异常, 错误原因{e}")
        return amis_ret(data={}, status=-1, msg="提交修改失败")

""" 删除数据库设备信息  """
@device_blue.route('/data_operation/<int:device_id>', methods=['DELETE'])
def delete_device_info(device_id):
    try:
        db.session.query(Device).filter_by(device_id=device_id).delete()
        db.session.commit()
        logging.critical(f"删除数据库中设备{device_id}信息成功")
        return amis_ret(data={}, status=0, msg="删除设备成功")
    except Exception as e:
        logging.error(f"SQL Error: try to delete device{device_id}, {e}")
        return amis_ret(data={}, status=-1, msg="删除设备失败")

# """"""""""""""""""""""""""""""""""   文件操作：文件   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   文件操作：文件   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   文件操作：文件   """"""""""""""""""""""""""""""""""
""" 获取数据库中上传文件信息  """
@device_blue.route('/file_operation/upload', methods=['GET'])
def get_uploadfiles_info():
    requst_args   = request.args

    orderBy  = requst_args.get('orderBy')
    orderDir = requst_args.get('orderDir')
    search_file_id    = request.values.get('file_id')
    search_file_name  = request.values.get('file_name')
    try:
        # 条件模糊查询
        db_obj = db.session.query(Uploadfiles).filter(
            Uploadfiles.file_id.like(f'%{search_file_id}%' if search_file_id else '%%'),
            Uploadfiles.file_name.like(f'%{search_file_name}%' if search_file_name else '%%'))

        if orderBy and orderDir:
            # 排序
            order = getattr(Uploadfiles, orderBy)        # equal: Uploadfiles.file_id
            order = getattr(order, orderDir)()           # equal: order=order.asc()
            db_obj = db_obj.order_by(order)

        # 查询数据库中所有设备信息
        files = db_obj.all()

        # 遍历文件列表中的文件是否存在，不存在则删除
        for file in reversed(files):
            if not os.path.exists(file.file_local_storage_path):
                delete_file = db.session.query(Uploadfiles).filter_by(file_id=file.file_id)
                delete_file.delete()
                files.remove(file)
        # delete record in db
        db.session.commit()

        files_count = db_obj.count()
        files_list = [file.to_dict() for file in files]
        ret_data = {
            "files_count"  : files_count,
            "files_list"   : files_list,
        }
        logging.critical("获取数据库中上传文件信息成功")
        return amis_ret(data=ret_data, status=0, msg="查询已上传文件成功")
    except Exception as e:
        logging.error(f"SQL Error: try to query existed upload file, 错误原因{e}")
        return amis_ret(data={}, status=-1, msg="查询已上传文件失败")

""" 接收来自web端上传的文件  """
@device_blue.route('/file_operation/upload', methods=['POST'])
def receive_file_from_web():
    # deal request args
    request_file_list = request.files.getlist("file")
    request_file = request_file_list[0]

    file_name               = request_file.filename
    file_source             = session.get("user_name")
    file_upload_time        = get_current_time_apply_to_filename()
    file_local_storage_path = Config.UPLOAD_FILE_STORAGE_PATH

    if os.path.exists(file_local_storage_path+file_name):
        logging.error(f"UPLOAD Error: try to upload existed file {file_name}")
        return amis_ret(data={}, status=-1, msg="已存在相同命名文件")
    else:
        try:
            # save file to local
            request_file.save(file_local_storage_path+file_name)

            # add record to db
            file_size = os.path.getsize(file_local_storage_path+file_name)
            db.session.add(Uploadfiles(file_name=file_name, file_size=file_size, file_source=file_source, file_upload_time=file_upload_time, file_local_storage_path=file_local_storage_path))
            db.session.commit()
            logging.critical(f"上传文件{file_name}至数据库成功")
            return amis_ret(data={}, status=0, msg="上传文件成功")

        except Exception as e:
            logging.error(f"UPLOAD Error: try to save file {file_name} and add record to db, 错误原因{e}")
            return amis_ret(data={}, status=-1, msg="上传文件失败")

""" 删除数据库设备信息  """
@device_blue.route('/file_operation/upload/<int:file_id>', methods=['DELETE'])
def delete_uploadfile(file_id):
    try:
        delete_file = db.session.query(Uploadfiles).filter_by(file_id=file_id)
        delete_file_first = delete_file.first()
        delete_file_name  = delete_file_first.file_local_storage_path + delete_file_first.file_name

        # delete record in db
        delete_file.delete()
        db.session.commit()

        # delete file
        if os.path.exists(delete_file_name):
            os.remove(delete_file_name)

        logging.critical(f"删除已上传数据库的文件{delete_file_name}成功")
        return amis_ret(data={}, status=0, msg="删除文件成功")

    except Exception as e:
        logging.error(f"SQL Error: try to delete file {delete_file_name}, 错误原因{e}")
        return amis_ret(data={}, status=-1, msg="删除文件失败")

# """"""""""""""""""""""""""""""""""   任务操作：任务   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   任务操作：任务   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   任务操作：任务   """"""""""""""""""""""""""""""""""
""" 获取数据库中设备对应的任务信息  """
@device_blue.route('/task_operation/<int:device_id>', methods=['GET'])
def get_tasks_info_by_deviceid(device_id):
    try:
        # 查询设备是否存在
        get_device = db.session.query(Device).filter_by(device_id=device_id).first()
        target_device_name = get_device.device_name

        try:
            # 查询Tasks表对应设备的任务信息
            db_obj = db.session.query(Tasks).filter_by(oper_device_id=device_id)
            tasks = db_obj.all()
            tasks_count = db_obj.count()

            # make ret
            # TODO 修改前端
            tasks_list = [task.to_dict() for task in tasks]
            ret_data = {
                "target_device_name" : target_device_name,
                "tasks_count"  : tasks_count,
                "tasks_list"   : tasks_list,
            }
            logging.critical("查询数据库中任务信息成功")
            return amis_ret(data=ret_data, status=0, msg="查询设备任务成功")
        except Exception as e:
            logging.error(f"SQL Error: try to query nonexisted task for device, id={device_id}, 错误原因{e}")
            return amis_ret(data={}, status=-1, msg="查询设备任务失败")
    except Exception as e:
        logging.error(f"SQL Error: try to query nonexisted device, id={device_id}, 错误原因{e}")
        return amis_ret(data={}, status=-1, msg="查询设备任务失败")

""" 添加device_id设备的任务信息  """
@device_blue.route('/task_operation/<int:device_id>', methods=['POST'])
def add_device_task_to_db(device_id):
    requst_body     = request.get_data()
    requst_args     = json.loads(requst_body)
    add_files_list  = str(requst_args["oper_file_id"]).split(",")
    try:
        # query device
        add_device = db.session.query(Device).filter_by(device_id=device_id).first()
        if add_device:
            add_task_list = []
            for file_id in add_files_list:
                try:
                    # query file
                    add_file = db.session.query(Uploadfiles).filter_by(file_id=file_id).first()

                    # 构建任务属性（名称、优先级）
                    add_task        = Tasks()
                    add_task_list.append(add_task)
                    db.session.add(add_task)
                    db.session.commit()

                    add_task.priority           = "0"
                    add_task.type               = Task_Type.DEVICE_WRITE.value
                    add_task.status             = "schedule"                    # success\pending\queue\schedule\fail

                    add_task.oper_device_id     = add_device.device_id
                    add_task.oper_device_name   = add_device.device_name
                    add_task.oper_file_id       = add_file.file_id
                    add_task.oper_file_path     = add_file.file_local_storage_path
                    add_task.oper_file_name     = add_file.file_name
                    add_task.oper_file_size     = add_file.file_size

                    add_task.submit_user        = session.get("user_name")
                    add_task.submit_time        = get_current_time_with_ms()
                    db.session.commit()
                    logging.critical(f"向数据库新增write任务({add_task.id})成功")
                except Exception as e:
                    logging.error(f"SQL Error: 尝试将任务（文件{file_id} 设备{add_device.device_id})写入数据库， 错误原因{e}")

            # commit to db
            db.session.commit()

            for task in add_task_list:
                try:
                    # 通过pika队列向控制软件发布任务
                    pika_channel_in.basic_publish(
                        exchange=Config.RABBITMQ_EXCHANGENAME_IN,   # RabbitMQ中所有的消息都要先通过交换机，空字符串表示使用默认的交换机
                        routing_key=Config.RABBITMQ_ROUTINGKEY_IN,  # 指定消息要发送到哪个queue
                        body=settle_device_event(task.id, Task_Type.DEVICE_WRITE.value, 
                            task.oper_device_id, task.oper_file_path + task.oper_file_name)) # 消息的内容

                    logging.critical(f"向pika队列写入任务信息{task.id}成功")
                except Exception as e:
                    logging.error(f"Task Error: 尝试发布任务到控制软件， 错误原因{e}")

            return amis_ret(data={}, status=0, msg="添加任务成功")
        else:
            raise
    except Exception as e:
        logging.error(f"SQL Error: try to find nonexisted device, id={device_id}, 错误原因{e}")
        return amis_ret(data={}, status=-1, msg="添加任务失败")

""" 删除task_id对应的任务记录  """
@device_blue.route('/task_operation/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        db.session.query(Tasks).filter_by(id=task_id).delete()
        db.session.commit()
        logging.warning(f"删除数据库中任务({task_id})成功")
        return amis_ret(data={}, status=0, msg="删除任务成功")
    except Exception as e:
        logging.error(f"删除数据库任务({task_id})异常， {e}")
        return amis_ret(data={}, status=-1, msg="删除任务失败")

""" 处理图表函数的参数  """
def dealargs_for_function_get_alldevices_taskinfo_for_chart():
    requst_args             = request.args
    selecttimestamprange    = requst_args.get('selectdaterange').split(",")    # 选择的日期范围
    selectunit              = requst_args.get('selectunit')                    # 选择的单位
    selectdevice            = requst_args.get('selectdevice').split(",")       # 选择的设备

    if selecttimestamprange and selectunit and selectdevice:
        # 处理日期范围
        start_datetime      = transfer_format_from_timestamp_to_datetime(int(selecttimestamprange[0]))
        end_datetime        = transfer_format_from_timestamp_to_datetime(int(selecttimestamprange[1]))
        diff_datetime       = cal_difftime_between_datetime(start_datetime, end_datetime)

        # 处理单位
        size_divisior = 1
        if selectunit == "B":
            size_divisior = 1
        elif selectunit == "KB":
            size_divisior = 1024
        elif selectunit == "MB":
            size_divisior = 1024 * 1024
        elif selectunit == "GB":
            size_divisior = 1024  * 1024 * 1024

        # 处理设备
        selectdeviceid_list = []
        selectdevicename_list = []
        selectdevicedesc_list = []
        for device_id in selectdevice:
            try:
                # 查询设备是否存在
                device_obj = db.session.query(Device).filter_by(device_id=device_id).first()
                selectdeviceid_list.append(device_obj.device_id)
                selectdevicename_list.append(device_obj.device_name)
                selectdevicedesc_list.append(device_obj.device_description)
            except:
                pass
    return selectunit, start_datetime, end_datetime, diff_datetime, size_divisior, selectdeviceid_list, selectdevicename_list, selectdevicedesc_list

""" 获取数据库中设备任务的设备与总流量图表  """
@device_blue.route('/task_operation/chart1', methods=['GET'])
def get_alldevices_taskinfo_for_chart1():
    selectunit, start_datetime, end_datetime, diff_datetime, size_divisior, selectdeviceid_list, selectdevicename_list, selectdevicedesc_list = dealargs_for_function_get_alldevices_taskinfo_for_chart()
    if selectdeviceid_list:
        # 初始化echarts图表
        statistical_item_list = ['任务总数', '流量总数', '平均传输速率']
        ret_data = {
            "title": {"text": "设备-流量情况"},
            "tooltip":
            {
                "trigger":"axis",
                "axisPointer":{"type":"shadow"}
            },
            "toolbox":{"show":"true","feature":{"saveAsImage":{}}},
            "legend": {"data":[],},
            "xAxis":
            {
                "type":"category",
                "name":"设备",
                "data": statistical_item_list,
                "axisTick":
                {
                    "alignWithLabel": "true"
                }
            },
            "yAxis":{"type": 'value',},
            "series":[],
        }

        # 遍历选择的设备
        task_count_list     = [0] * len(selectdeviceid_list)        # 统计：任务总数
        dataflow_count_list = [0] * len(selectdeviceid_list)        # 统计：流量
        transfer_speed_list = [0] * len(selectdeviceid_list)        # 统计：平均传输速率
        for idx, device_id in enumerate(selectdeviceid_list):
            try:
                # 查询Tasks表对应设备的任务信息
                db_obj = db.session.query(Tasks).filter_by(oper_device_id=device_id).filter(and_(Tasks.finish_time>start_datetime, 
                                                                                                 Tasks.finish_time<end_datetime, 
                                                                                                 Tasks.status=="success"))

                tasks = db_obj.all()
                for task in tasks:
                    task_count_list[idx]     += 1
                    dataflow_count_list[idx] += float(task.oper_file_size)
                    transfer_speed_list[idx] += float(task.transfer_rate)
            except Exception as e:
                logging.error(f"渲染Chart1时查询设备{idx}的历史任务出错，错误原因{e}")

            dataflow_count_list[idx] = round(dataflow_count_list[idx] / size_divisior, 2)
            if task_count_list[idx] > 0:
                transfer_speed_list[idx] = round(transfer_speed_list[idx] / task_count_list[idx] / size_divisior, 2)

            ret_data["series"].append({
                    "name": selectdevicedesc_list[idx],
                    "type":"bar",
                    "data": [task_count_list[idx], dataflow_count_list[idx], transfer_speed_list[idx]],
                    "showBackground": "true",
                    "emphasis": {"focus": 'series'},
                    "label": {"show": "true","position": 'top'},
                })
        ret_data["legend"]["data"] = selectdevicedesc_list

        return amis_ret(data=ret_data, status=0, msg="查询设备任务图表成功")
    else:
        return amis_ret(data={}, status=-1, msg="查询设备任务图表失败")

""" 获取数据库中设备任务的日期与设备流量图表  """
@device_blue.route('/task_operation/chart2', methods=['GET'])
def get_alldevices_taskinfo_for_chart2():
    selectunit, start_datetime, end_datetime, diff_datetime, size_divisior, selectdeviceid_list, selectdevicename_list, selectdevicedesc_list = dealargs_for_function_get_alldevices_taskinfo_for_chart()

    # 监测查询设备列表是否为空
    if not selectdeviceid_list:
        return amis_ret(data={}, status=-1, msg="查询设备任务图表失败")

    # 初始化echarts图表
    ret_data = {
        "title": {"text": "日期-流量情况"},
        "tooltip":
        {
            "trigger":"axis",
            "axisPointer":{"type":"cross"}
        },
        "toolbox":{"show":"true","feature":{"saveAsImage":{}}},
        "legend": {"data":[],},
        "xAxis":
        {
            "type":"category",
            "boundaryGap":"false",
        },
        "yAxis":
        {
            "type":"value",
            "name":"数据流量/ " + selectunit,
            "axisLabel":{"formatter":"{value}"},
            "axisPointer":{"snap":"true"},
        },
        "series":[],
    }

    if diff_datetime > (24 * 60 * 60) : # ! 时间差大于1天
        ret_data["xAxis"]["name"] = "日期/ 天"
        exp_format = "D"
    elif diff_datetime > (60 * 60)    : # ! 时间差大于1小时
        ret_data["xAxis"]["name"] = "日期/ 小时"
        exp_format = "H"
    elif diff_datetime > (60)         : # ! 时间差大于1分钟
        ret_data["xAxis"]["name"] = "日期/ 分钟"
        exp_format = "M"
    else:                               # ! 时间差处于[0,60秒]
        ret_data["xAxis"]["name"] = "日期/ 秒"
        exp_format = "S"

    selectdate_list, selectdate_brief_list = generate_dateinterval_by_datetime(start_datetime, end_datetime, exp_format)
    ret_data["xAxis"]["data"] = selectdate_brief_list

    # 遍历选择的设备
    for idx, device_id in enumerate(selectdeviceid_list):
        dataflow_list    = [0.0] * len(selectdate_list)
        try:
            # 查询Tasks表对应设备的任务信息
            db_obj = db.session.query(Tasks).filter_by(oper_device_id=device_id).filter(and_(Tasks.finish_time>start_datetime, 
                                                                                             Tasks.finish_time<end_datetime, 
                                                                                             Tasks.status=="success"))

            tasks = db_obj.all()
            for task in tasks:

                task_finish_date = transfer_format_from_datetime_with_ms_to_date(task.finish_time, exp_format)
                if task_finish_date in selectdate_list:
                    dataflow_list[selectdate_list.index(task_finish_date)] += round(float(task.oper_file_size) / size_divisior, 2)

            ret_data["legend"]["data"].append(selectdevicedesc_list[idx])
            ret_data["series"].append({
                    "name": selectdevicedesc_list[idx],
                    "type":"line",
                    "smooth":"true",
                    "data":dataflow_list,
                    "markPoint": {"data": [{ "type": 'max', "name": 'Max' }]},
                })
        except Exception as e:
            logging.error(f"渲染Chart2时查询设备{idx}的历史任务出错，错误原因{e}")

    if ret_data["series"]:
        return amis_ret(data=ret_data, status=0, msg="查询设备任务图表成功")
    else:
        logging.error("Chart Error: try to query task chart for device")
        return amis_ret(data=ret_data, status=-1, msg="查询设备任务图表失败")


# """"""""""""""""""""""""""""""""""   响应操作：事件   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   响应操作：事件   """"""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""   响应操作：事件   """"""""""""""""""""""""""""""""""
def cb(ch, method, properties, body):
    # 1、解析来自控制应用的事件
    try:
        body = body.decode("utf-8").replace("\n", "").replace("\t", "")
        task_id, task_type, oper_device, oper_action, oper_status, other_info = parse_device_event(body)
        logging.critical(f"PIKA读取到消息({body})")
    except Exception as e:
        logging.error(f"解析来自控制应用的事件({body})错误, {e}")

    # 2、查询数据中设备情况
    with app.app_context():
        try:
            # 3、查找设备
            device_obj = db.session.query(Device).filter_by(device_id=oper_device).first()
            if not device_obj:
                raise Exception(f"未查找到设备")
            
            # 4、查找任务
            if task_type == Task_Type.DEVICE_READ.value:
                add_task                    = Tasks()
                add_task.type               = Task_Type.DEVICE_READ.value
                add_task.oper_device_id     = oper_device
                db.session.add(add_task)
                db.session.commit()
                task_id = add_task.id
            task_obj = db.session.query(Tasks).filter_by(id=task_id).first()
            if not task_obj:
                raise Exception("未查找到任务")

            # 根据任务类型进行处理
            task_obj.status                 = oper_status
            task_obj.finish_time            = get_current_time_with_ms()

            if      task_type == Task_Type.DEVICE_OPEN.value       or \
                    task_type == Task_Type.DEVICE_CLOSE.value :
                device_obj.device_status = '1' if device_obj.device_status == '0' else '0'

            elif    task_type == Task_Type.DEVICE_READ.value:
                task_obj.oper_device_name = device_obj.device_name
                # 设置操作的文件
                pass

            elif task_type == Task_Type.DEVICE_WRITE.value :
                # 计算传输速率等
                pass

        except Exception as e:
            logging.error(f"PIKA接收到控制应用的任务{task_id}出现错误，{e}")
        finally:
            db.session.commit()

def pika_consumer(qu_name):
    pika_channel_out.basic_consume(queue=qu_name, on_message_callback=cb, auto_ack=True)
    pika_channel_out.start_consuming()

# 监听pika
th = threading.Thread(target=pika_consumer, args=(Config.RABBITMQ_QUEUENAME_OUT, ))
th.start()