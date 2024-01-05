# -*- coding: utf-8 -*-
'''
<!-- Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved  -->
Author: TheDraco
Date: 2022-12-06 17:27:51
LastEditTime: 2023-01-18 14:19:39
Description: 
FilePath: /10_flask/app/models/models.py
'''
from enum import Enum
from .. import db

class User(db.Model):
    """ user class  """
    # 创建表
    __tablename__ = "users"

    # 创建字段
    user_id         = db.Column(db.Integer   , primary_key=True)             # users表中的id字段(主键)
    user_name       = db.Column(db.String(64), nullable=False, index=True)   # users表中的user_name字段
    user_password   = db.Column(db.String(64), nullable=False, index=True)   # users表中的password字段
    user_profile    = db.Column(db.String(64), nullable=False, index=True)   # users表中的gender字段(有索引)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.user_name)
        
    def to_dict(self):
        resp_dict = {
            "user_id"      : self.user_id,
            "user_name"    : self.user_name,
            "user_password": self.user_password,
            "user_profile" : self.user_profile
        }
        return resp_dict

class Device(db.Model):
    """ device class  """
    # 创建表
    __tablename__ = "devices"

    # 创建字段
    device_id            = db.Column(db.Integer   , primary_key=True)             # devices表中的id字段(主键)
    device_name          = db.Column(db.String(64), nullable=False, index=True)   # devices表中的name字段
    device_type          = db.Column(db.String(64), nullable=False, index=True)   # devices表中的type字段
    device_status        = db.Column(db.String(64), nullable=False, index=True)   # devices表中的status字段
    device_property      = db.Column(db.String(64), nullable=False, index=True)   # devices表中的property字段
    device_description   = db.Column(db.String(64), nullable=False, index=True)   # devices表中的description字段
    last_work_time       = db.Column(db.String(64), nullable=False, index=True)   # devices表中的last_work_time字段
    last_edit_time       = db.Column(db.String(64), nullable=False, index=True)   # devices表中的last_edit_time字段
    
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.device_name)
        
    def to_dict(self):
        resp_dict = {
            "device_id"         : self.device_id,
            "device_name"       : self.device_name,
            "device_type"       : self.device_type,
            "device_status"     : self.device_status,
            "device_property"   : self.device_property,
            "device_description": self.device_description,
            "last_work_time"    : self.last_work_time,
            "last_edit_time"    : self.last_edit_time
        }
        return resp_dict
        
    def modify_from_dict(self, json_dict):
        # self.device_id          = json_dict["device_id"]
        self.device_name        = json_dict["device_name"]
        self.device_type        = json_dict["device_type"]
        self.device_status      = json_dict["device_status"]
        self.device_property    = json_dict["device_property"]
        self.device_description = json_dict["device_description"]
        self.last_work_time     = json_dict["last_work_time"]
        self.last_edit_time     = json_dict["last_edit_time"]


class Uploadfiles(db.Model):
    """ upload files class  """
    # 创建表
    __tablename__ = "uploadfiles"

    # 创建字段
    file_id                 = db.Column(db.Integer   , primary_key=True)             # uploadfiles表中的id字段(主键)
    file_name               = db.Column(db.String(64), nullable=False, index=True)   # uploadfiles表中的name字段
    file_size               = db.Column(db.String(64), nullable=False, index=True)   # uploadfiles表中的size字段
    file_source             = db.Column(db.String(64), nullable=False, index=True)   # uploadfiles表中的source字段
    file_upload_time        = db.Column(db.String(64), nullable=False, index=True)   # uploadfiles表中的upload_time字段
    file_local_storage_path = db.Column(db.String(64), nullable=False, index=True)   # uploadfiles表中的local_storage_path字段

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.file_name)

    def to_dict(self):
        resp_dict = {
            "file_id"                   : self.file_id,
            "file_name"                 : self.file_name,
            "file_size"                 : self.file_size,
            "file_source"               : self.file_source,
            "file_upload_time"          : self.file_upload_time,
            "file_local_storage_path"   : self.file_local_storage_path,
        }
        return resp_dict


class Task_Type(Enum):
    DEVICE_POWER_ON  = "power on"       # 0x1, 上电
    DEVICE_POWER_OFF = "power off"      # 0x2, 下电
    DEVICE_OPEN      = "open"           # 0x3, 打开
    DEVICE_CLOSE     = "close"          # 0x4  关闭
    DEVICE_CONFIG    = "config"         # 0x5  配置
    DEVICE_WRITE     = "write"          # 0x6  写入
    DEVICE_READ      = "read"           # 0x7  读取
    DEVICE_READYREAD = "readyread"      # 0x8  可读
    DEVICE_OTHER     = "other"          # 0x9  其他
    
class Tasks(db.Model):
    # 创建表
    __tablename__ = "tasks"

    # 创建字段
    id                      = db.Column(db.Integer   , primary_key=True)    # tasks表中的id字段(主键)      
    priority                = db.Column(db.Integer) 
    type                    = db.Column(db.String(64))          
    status                  = db.Column(db.String(64))
    submit_user             = db.Column(db.String(64))     
    submit_time             = db.Column(db.String(64))         
    sched_time              = db.Column(db.String(64))         
    sched_finish_time       = db.Column(db.String(64))         
    finish_time             = db.Column(db.String(64))    
    oper_device_id          = db.Column(db.Integer)       
    oper_device_name        = db.Column(db.String(64))      
    oper_file_id            = db.Column(db.Integer)   
    oper_file_path          = db.Column(db.String(64))        
    oper_file_name          = db.Column(db.String(64))     
    oper_file_size          = db.Column(db.String(64))  
    transfer_rate           = db.Column(db.String(64))     
    corrected_transfer_rate = db.Column(db.String(64)) 
    remark                  = db.Column(db.String(64)) 

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.task_name)

    def to_dict(self):
        resp_dict = {
            "id"                        : self.id,
            "priority"                  : self.priority,
            "type"                      : self.type,
            "status"                    : self.status,

            "submit_user"               : self.submit_user,
            "submit_time"               : self.submit_time,
            "sched_time"                : self.sched_time,
            "sched_finish_time"         : self.sched_finish_time,
            "finish_time"               : self.finish_time,

            "oper_device_id"            : self.oper_device_id,
            "oper_device_name"          : self.oper_device_name,
            "oper_file_id"              : self.oper_file_id,
            "oper_file_path"            : self.oper_file_path,
            "oper_file_name"            : self.oper_file_name,
            "oper_file_size"            : self.oper_file_size,

            "transfer_rate"             : self.transfer_rate,
            "corrected_transfer_rate"   : self.corrected_transfer_rate,

            "remark"                    : self.remark
        }
        return resp_dict