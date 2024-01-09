import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Content-Type": "application/json"
}

device5_post_params = {
    "url" : "http://localhost:80/device/task_operation/5",
    "headers" : headers,
    "json" : {
        "oper_file_id": 193
    }
}

device6_post_params = {
    "url" : "http://localhost:80/device/task_operation/6",
    "headers" : headers,
    "json" : {
        "oper_file_id": 193
    }
}

device7_post_params = {
    "url" : "http://localhost:80/device/task_operation/7",
    "headers" : headers,
    "json" : {
        "oper_file_id": 189
    }
}

device8_post_params = {
    "url" : "http://localhost:80/device/task_operation/8",
    "headers" : headers,
    "json" : {
        "oper_file_id": 190
    }
}

for t in range(500):

    # response = requests.post(**device5_post_params)
    response = requests.post(**device6_post_params)
    response = requests.post(**device7_post_params)
    response = requests.post(**device8_post_params)
    # print(response.text)

    time.sleep(0.1)