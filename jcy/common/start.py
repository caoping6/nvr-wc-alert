import time

import requests
from heartbeat import Heartbeat
from datetime import datetime, timezone, timedelta
from wechat import WeChatClient
from logger_util import Logger
import threading
import json

logger = Logger("alert.log")

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

hb = Heartbeat()


def loop_heartbeat():
    while True:
        logger.info("send to Heartbeat...")
        hb.send_heartbeat()
        time.sleep(5)


def loop_check(request_json):
    while True:
        logger.info("send to Heartbeat...")
        response = hb.check(request_json)
        result = json.loads(response.text)
        if result is not None and result.get("result") == 'success':
            data = result.get("data")
            request_json['reader_id'] = data["reader_id"]
            request_json['sequence'] = data["sequence"]
            request_json['lap_number'] = data["lap_number"]

            alarm_list = data["alarm_list"]
            for alarm in alarm_list:
                if "face_alarm" in alarm.keys():
                    face_alarms = alarm["face_alarm"]
                    alarm_time = alarm["time"]
                    for face_alarm in face_alarms:
                        face_id = face_alarm["Id"]
                        if face_id > 0:
                            face_name = face_alarm["Name"]
                            face_phone = face_alarm["Phone"]
                            face_time = datetime.strptime(alarm_time, "%m/%d/%Y %H:%M:%S")
                            web_client = WeChatClient()
                            web_client.get_token()
                            web_client.send_msg(face_phone, face_name, face_time)

        time.sleep(5)


def check_first():
    response = hb.check({})
    result = json.loads(response.text)
    if result is not None and result.get("result") == 'success':
        data = result.get("data")
        reader_id = data["reader_id"]
        sequence = data["sequence"]
        lap_number = data["lap_number"]

        request_json = {
            "subscribe_ai_metadata": True,
            "reader_id": reader_id,
            "sequence": sequence,
            "lap_number": lap_number
        }
        thread = threading.Thread(target=loop_check, args=request_json)
        thread.start()

    else:
        hb.login()


if __name__ == '__main__':
    # 获取当前日期和时间
    logger.info("程序开始...")
    # 创建并启动心跳检测线程
    check_first()
