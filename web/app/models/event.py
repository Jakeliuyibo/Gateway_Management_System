# -*- coding: utf-8 -*-

from enum import Enum
from flask import json

def settle_device_event(task_id: int, event: str, device: int, action: str):
    task = {
                "id"        :   task_id ,
                "type"      :   str(event),
                "device"    :   device,  
                "action"    :   str(action),
                "status"    :   "",
                "other"     :   "",
            }
    return str(task).replace("\'", "\"")

def parse_device_event(event_str: str):
    event = json.loads(event_str)
    id = event.get("id")
    type = event.get("type")
    device = event.get("device")
    action = event.get("action")
    status = event.get("status")
    other = event.get("other")
    return id, type, device, action, status, other