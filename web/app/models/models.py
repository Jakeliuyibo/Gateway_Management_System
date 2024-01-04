# -*- coding: utf-8 -*-
'''
<!-- Copyright (C) 2022 - 2023 liuyibo. All Rights Reserved  -->
Author: TheDraco
Date: 2022-12-06 17:27:51
LastEditTime: 2023-01-18 14:19:39
Description: 
FilePath: /10_flask/app/models/models.py
'''
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


class Tasks(db.Model):
    """ tasks class  """
    # 创建表
    __tablename__ = "tasks"

    # 创建字段
    task_id                     = db.Column(db.Integer   , primary_key=True)    # tasks表中的id字段(主键)
    task_name                   = db.Column(db.String(64))                      # tasks表中的name字段
    task_priority               = db.Column(db.String(64))                      # tasks表中的priority字段

    source_file_id              = db.Column(db.Integer)                         # tasks表中的file_id字段
    source_file_name            = db.Column(db.String(64))                      # tasks表中的file_name字段
    source_file_size            = db.Column(db.String(64))                      # tasks表中的file_size字段
    source_file_path            = db.Column(db.String(64))                      # tasks表中的file_path字段

    target_device_id            = db.Column(db.Integer)                         # tasks表中的device_id  字段
    target_device_name          = db.Column(db.String(64))                      # tasks表中的device_name字段

    task_status                 = db.Column(db.Integer)                         # tasks表中的status        字段
    task_submit_time            = db.Column(db.String(64))                      # tasks表中的submit_time   字段
    task_submit_source          = db.Column(db.String(64))                      # tasks表中的submit_source 字段
    task_execute_time           = db.Column(db.String(64))                      # tasks表中的execute_time  字段
    task_finish_time            = db.Column(db.String(64))                      # tasks表中的finish_time   字段
    task_transfer_speed         = db.Column(db.String(64))                      # tasks表中的transfer_speed字段

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.task_name)

    def to_dict(self):
        resp_dict = {
            "task_id"                   : self.task_id,
            "task_name"                 : self.task_name,
            "task_priority"             : self.task_priority,

            "source_file_id"            : self.source_file_id,
            "source_file_name"          : self.source_file_name,
            "source_file_size"          : self.source_file_size,
            "source_file_path"          : self.source_file_path,

            "target_device_id"          : self.target_device_id,
            "target_device_name"        : self.target_device_name,

            "task_status"               : self.task_status,
            "task_submit_time"          : self.task_submit_time,
            "task_submit_source"        : self.task_submit_source,
            "task_execute_time"         : self.task_execute_time,
            "task_finish_time"          : self.task_finish_time,
            "task_transfer_speed"       : self.task_transfer_speed,
        }
        return resp_dict