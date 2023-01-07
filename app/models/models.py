'''
Author: TheDraco
Date: 2022-12-06 17:27:51
LastEditTime: 2023-01-05 18:13:46
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
    user_name       = db.Column(db.String(64), nullable=False, index=True)   # users表中的username字段
    user_password   = db.Column(db.String(64), nullable=False, index=True)   # users表中的password字段
    user_profile    = db.Column(db.String(64), nullable=False, index=True)   # users表中的gender字段(有索引)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)