import time

from heartbeat import Heartbeat
from datetime import datetime, time
import time
from wechat import WeChatClient
from logger_util import Logger
import threading
import json
from read_config import ReadConfig

logger = Logger("../logs/alert.log")

hb = Heartbeat()
clock_dict = ReadConfig("clock_time", 'jcy/conf/alert.conf').get_config()
file_cache = 'clock_cache.json'


# 将数据写入JSON文件
def write_to_json_file(data):
    with open(file_cache, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# 从JSON文件读取数据
def read_from_json_file():
    with open(file_cache, 'r') as file:
        return json.load(file)


def loop_heartbeat():
    while True:
        try:
            logger.info("send to Heartbeat...")
            # hb.send_heartbeat()
            if is_clock_time("00:05-00:10", datetime.now().time()):
                write_to_json_file({})
            time.sleep(5)
        except Exception as e:
            logger.error(f"loop heartbeat failed: {e}")
            time.sleep(2)


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
            parse_face_alarm(data)
        else:
            break
        time.sleep(5)


def parse_face_alarm(data):
    if "alarm_list" not in data:
        return
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
                    check_time_alert(face_name, face_phone, face_time)


def check_time_alert(face_name, face_phone, face_time):
    clock_json = read_from_json_file()
    # 上午上班打卡
    if is_clock_time(clock_dict['morning_clock_in'], face_time.time()):
        morning_clock_in_key = 'morning_clock_in_' + face_phone
        if has_clock(morning_clock_in_key) is not True:
            web_client = WeChatClient()
            web_client.get_token()
            web_client.send_msg(face_phone, face_name, face_time)
            clock_json[morning_clock_in_key] = face_time
    # 上午下班打卡
    if is_clock_time(clock_dict['morning_clock_out'], face_time.time()):
        morning_clock_out_key = 'morning_clock_out_' + face_phone
        if has_clock(morning_clock_out_key) is not True:
            web_client = WeChatClient()
            web_client.get_token()
            web_client.send_msg(face_phone, face_name, face_time)
            clock_json[morning_clock_out_key] = face_time
    # 下午上班打卡
    if is_clock_time(clock_dict['afternoon_clock_in'], face_time.time()):
        afternoon_clock_in_key = 'afternoon_clock_in_' + face_phone
        if has_clock(afternoon_clock_in_key) is not True:
            web_client = WeChatClient()
            web_client.get_token()
            web_client.send_msg(face_phone, face_name, face_time)
            clock_json[afternoon_clock_in_key] = face_time
    # 下午下班打卡
    if is_clock_time(clock_dict['afternoon_clock_out'], face_time.time()):
        afternoon_clock_out_key = 'afternoon_clock_out_' + face_phone
        if has_clock(afternoon_clock_out_key) is not True:
            web_client = WeChatClient()
            web_client.get_token()
            web_client.send_msg(face_phone, face_name, face_time)
            clock_json[afternoon_clock_out_key] = face_time
    write_to_json_file(clock_json)


def is_clock_time(clock_time, face_time):
    time_arr = clock_time.split('-')
    start_time = datetime.strptime(time_arr[0], '%H:%M').time()
    end_time = datetime.strptime(time_arr[1], '%H:%M').time()
    return start_time <= face_time <= end_time


def has_clock(clock_key):
    clock_json = read_from_json_file()
    if clock_key in clock_json:
        return True
    return False


def check_first():
    response = hb.check({})
    result = json.loads(response.text)
    if result is not None and result.get("result") == 'success':
        data = result.get("data")
        reader_id = data["reader_id"]
        sequence = data["sequence"]
        lap_number = data["lap_number"]

        request_json = {
            "data": {
                "subscribe_ai_metadata": True,
                "reader_id": reader_id,
                "sequence": sequence,
                "lap_number": lap_number
            }
        }
        loop_check(request_json)
    else:
        hb.login()
    time.sleep(5)


if __name__ == '__main__':
    logger.info("start process...")
    thread = threading.Thread(target=loop_heartbeat)
    thread.start()
    time.sleep(10)
    logger.info("start check...")
    while True:
        try:
            check_first()
        except Exception as e:
            logger.error(f"check first failed: {e}")
            time.sleep(2)


