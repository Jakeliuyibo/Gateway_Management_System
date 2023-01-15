# -*- coding: utf-8 -*-
'''
Author: TheDraco
Date: 2022-12-06 17:27:51
LastEditTime: 2023-01-15 16:03:44
Description: 
FilePath: /10_flask/app/models/models.py
'''
from app import db

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
    """ user class  """
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