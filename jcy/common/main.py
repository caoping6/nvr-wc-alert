from heartbeat import Heartbeat
from datetime import datetime, time
import time
from wechat import WeChatClient
from logger_util import Logger
import json
from read_config import ReadConfig
import traceback

logger = Logger("../logs/alert.log")

hb = Heartbeat()
clock_dict = ReadConfig("clock_time", 'jcy/conf/alert.conf').get_config()
file_cache = 'clock_cache.json'
web_client = WeChatClient()
face_sequence=0
face_lap_number=0

# 将数据写入JSON文件
def write_to_json_file(data):
    with open(file_cache, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# 从JSON文件读取数据
def read_from_json_file():
    with open(file_cache, 'r') as file:
        return json.load(file)


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
                    try:
                        face_name = face_alarm["Name"]
                        face_phone = face_alarm["Phone"]
                        check_time_alert(face_name, face_phone, alarm_time)
                    except Exception as exp:
                        logger.error(f"check first failed: {exp}")


def check_time_alert(face_name, face_phone, alarm_time):
    logger.info(f"Check face and alert: face_name={face_name} , face_phone={face_phone}, alarm_time={alarm_time}")
    open_id = web_client.openid_dict.get(face_phone)
    if open_id is None:
        logger.warning(f"Check face openid is not exists: face_phone={face_phone}")
        return
    clock_json = read_from_json_file()
    # 上午上班打卡
    face_time = datetime.strptime(alarm_time, "%m/%d/%Y %H:%M:%S")
    if is_clock_time(clock_dict['morning_clock_in'], face_time.time()):
        morning_clock_in_key = 'morning_clock_in_' + face_phone
        if has_clock(morning_clock_in_key) is not True:
            send_wc_msg(face_name, face_phone, face_time)
            clock_json[morning_clock_in_key] = alarm_time
    # 上午下班打卡
    elif is_clock_time(clock_dict['morning_clock_out'], face_time.time()):
        morning_clock_out_key = 'morning_clock_out_' + face_phone
        if has_clock(morning_clock_out_key) is not True:
            send_wc_msg(face_name, face_phone, face_time)
            clock_json[morning_clock_out_key] = alarm_time
    # 下午上班打卡
    elif is_clock_time(clock_dict['afternoon_clock_in'], face_time.time()):
        afternoon_clock_in_key = 'afternoon_clock_in_' + face_phone
        if has_clock(afternoon_clock_in_key) is not True:
            send_wc_msg(face_name, face_phone, face_time)
            clock_json[afternoon_clock_in_key] = alarm_time
    # 下午下班打卡
    elif is_clock_time(clock_dict['afternoon_clock_out'], face_time.time()):
        afternoon_clock_out_key = 'afternoon_clock_out_' + face_phone
        if has_clock(afternoon_clock_out_key) is not True:
            send_wc_msg(face_name, face_phone, face_time)
            clock_json[afternoon_clock_out_key] = alarm_time
    else:
        logger.info(f"not in clock time: {e}")
    write_to_json_file(clock_json)


def send_wc_msg(face_name, face_phone, face_time):
    try:
        web_client.get_token()
        web_client.send_msg(face_phone, face_name, face_time)
    except Exception as exception:
        logger.error(f"send wechat failed: {exception}")


def is_clock_time(clock_time, face_time):
    time_arr = clock_time.split('-')
    start_time = datetime.strptime(time_arr[0], '%H:%M').time()
    end_time = datetime.strptime(time_arr[1], '%H:%M').time()
    return start_time <= face_time <= end_time


def is_clock_time_segment(clock_time):
    if is_clock_time(clock_dict['morning_clock_in'], clock_time) \
            or is_clock_time(clock_dict['morning_clock_out'], clock_time) \
            or is_clock_time(clock_dict['afternoon_clock_in'], clock_time) \
            or is_clock_time(clock_dict['afternoon_clock_out'], clock_time):
        return True
    else:
        return False


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
        sequence = face_sequence if face_sequence > 0 else data["sequence"]
        lap_number = face_lap_number if face_lap_number > 0 else data["lap_number"]

        request_json = {
            "data": {
                "subscribe_ai_metadata": True,
                "reader_id": reader_id,
                "sequence": sequence,
                "lap_number": lap_number
            }
        }
        loop_check(request_json)


def loop_check(request_json):
    global face_sequence
    global face_lap_number
    # 获取当前时间戳
    start_time = time.time()
    while True:
        # 获取当前时间和开始时间之间的差值
        elapsed_time = time.time() - start_time
        # 检查是否已经超过30秒
        if elapsed_time > 28:
            logger.info("Exiting loop after 30 seconds.")
            break
        logger.info("loop check second...")
        response = hb.check(request_json)
        if response.status_code != 200:
            face_sequence = 0
            face_lap_number = 0
            return
        result = json.loads(response.text)
        if result is not None and result.get("result") == 'success':
            data = result.get("data")
            reader_id = data["reader_id"]
            sequence = data["sequence"]
            lap_number = data["lap_number"]
            logger.info(f"check result reader_id= {reader_id}, sequence={sequence}, lap_number={lap_number}")
            request_json['reader_id'] = data["reader_id"]
            request_json['sequence'] = data["sequence"]
            request_json['lap_number'] = data["lap_number"]
            face_sequence = sequence
            face_lap_number = lap_number
            parse_face_alarm(data)
        else:
            break


if __name__ == '__main__':
    logger.info("start process...")
    while True:
        try:
            if is_clock_time("00:05-00:10", datetime.now().time()):
                write_to_json_file({})
            # 不再时间段内直接退出
            if is_clock_time_segment(datetime.now().time()) is not True:
                time.sleep(2)
                continue
            logger.info("send heartbeat then check...")
            hb.send_heartbeat()
            check_first()
        except Exception as e:
            logger.error(f"check first failed: {traceback.format_exc()}")