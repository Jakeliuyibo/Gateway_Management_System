# -*- coding: utf-8 -*-

from enum import Enum
from flask import json

def settle_device_event(task_id: int, event: str, device: str, action: str):
    task = {
                "id"        :   task_id ,
                "type"      :   str(event),
                "device"    :   str(device),  
                "action"    :   str(action),
            }
    return str(task).replace("\'", "\"")

