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

def parse_device_event_other_info(other_str: str):
    info = json.loads(other_str)
    sched_time = info.get("sched_time")
    sched_finish_time = info.get("sched_finish_time")
    trans_bytes = info.get("trans_bytes")
    recv_bytes = info.get("recv_bytes")
    file_full_path = info.get("file_full_path")
    file_path = info.get("file_path")
    file_name = info.get("file_name")
    file_size = info.get("file_size")
    return sched_time, sched_finish_time, trans_bytes, recv_bytes, file_full_path, file_path, file_name, file_size
