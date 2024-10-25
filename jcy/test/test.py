import time
import threading
import json
from jcy.common.logger_util import Logger

logger = Logger("alert.log")


def loop_heartbeat():
    while True:
        logger.info("send to Heartbeat...")
        time.sleep(5)


def check(data):
    if "alarm_lists" not in data:
        return
    alarm_list = data["alarm_list"]
    for alarm in alarm_list:
        if "face_alarm" in alarm.keys():
            face_alarms = alarm["face_alarm"]
            alarm_time = alarm["time"]
            for face_alarm in face_alarms:
                face_id = face_alarm["Id"]
                if face_id > 0:
                    print("name= " + face_alarm["Name"])

if __name__ == '__main__':
    # 获取当前日期和时间
    logger.info("程序开始...")
    # 创建并启动心跳检测线程
    thread = threading.Thread(target=loop_heartbeat, args=())
    thread.start()

    response = '{"result":"success","data":{"alarm_list":[{"time":"10/21/2024 10:20:35","channel_alarm":[{"channel":"CH1","record_flag":{"s":"G"}},{"channel":"CH2","record_flag":{}},{"channel":"CH3","record_flag":{}},{"channel":"CH4","record_flag":{"s":"R","r":"SR"}},{"channel":"CH5","record_flag":{}},{"channel":"CH6","record_flag":{"s":"R","r":"SR"}},{"channel":"CH7","record_flag":{}},{"channel":"CH8","record_flag":{}},{"channel":"CH9","record_flag":{"s":"R","r":"SR"}},{"channel":"CH10","record_flag":{"s":"R","r":"SR"}},{"channel":"CH11","record_flag":{}},{"channel":"CH12","record_flag":{}},{"channel":"CH13","record_flag":{}},{"channel":"CH14","record_flag":{}},{"channel":"CH15","record_flag":{}},{"channel":"CH16","record_flag":{}}]},{"time":"10/21/2024 10:20:39","channel_alarm":[{"channel":"CH1","record_flag":{"s":"G"}},{"channel":"CH2","record_flag":{}},{"channel":"CH3","record_flag":{}},{"channel":"CH4","record_flag":{"s":"R","r":"SR"}},{"channel":"CH5","record_flag":{}},{"channel":"CH6","record_flag":{"s":"R","r":"SR"}},{"channel":"CH7","record_flag":{}},{"channel":"CH8","record_flag":{}},{"channel":"CH9","record_flag":{"s":"R","r":"SR"}},{"channel":"CH10","record_flag":{"s":"R","r":"SR"}},{"channel":"CH11","record_flag":{}},{"channel":"CH12","record_flag":{}},{"channel":"CH13","record_flag":{}},{"channel":"CH14","record_flag":{}},{"channel":"CH15","record_flag":{}},{"channel":"CH16","record_flag":{}}]},{"time":"10/21/2024 10:20:40","face_alarm":[{"Id":120,"GrpId":8,"Sex":1,"Age":20,"Name":"岳俊伟","GrpName":"办公室","Policy":0,"Country":"","NativePlace":"","IdCode":"","Job":"","Phone":"","Email":"","Domicile":"","Remark":"7","FaceRect":{"X":1687,"Y":5263,"Width":359,"Height":777},"AlarmFlags":6,"MatchedFtVersion":1513229032,"OverMaxCount":false,"AppearCnt":0,"StartTime":1729506030,"EndTime":1729506040,"Similarity":98.2818832397461,"SnapId":2232,"SnapChn":10,"SnapFtVersion":12591105,"Gender":1,"SnapAge":-1,"SnapAgeGrp":3,"Expression":-1,"Hair":2,"Hat":1,"GlassType":1,"MouthMask":1,"Mustache":1,"GrpEnableAlarm":true}]},{"time":"10/21/2024 10:20:41","channel_alarm":[{"channel":"CH1","record_flag":{"s":"G"}},{"channel":"CH2","record_flag":{}},{"channel":"CH3","record_flag":{}},{"channel":"CH4","record_flag":{"s":"R","r":"SR"}},{"channel":"CH5","record_flag":{}},{"channel":"CH6","record_flag":{"s":"R","r":"SR"}},{"channel":"CH7","record_flag":{}},{"channel":"CH8","record_flag":{}},{"channel":"CH9","record_flag":{"s":"R","r":"SR"}},{"channel":"CH10","record_flag":{"s":"R","r":"SR"}},{"channel":"CH11","record_flag":{}},{"channel":"CH12","record_flag":{}},{"channel":"CH13","record_flag":{}},{"channel":"CH14","record_flag":{}},{"channel":"CH15","record_flag":{}},{"channel":"CH16","record_flag":{}}]},{"time":"10/21/2024 10:20:41","face_alarm":[{"Id":-1,"GrpId":4,"Sex":1,"Age":20,"Name":"","GrpName":"陌生人","Policy":2,"Country":"","NativePlace":"","IdCode":"","Job":"","Phone":"","Email":"","Domicile":"","Remark":"","FaceRect":{"X":7875,"Y":4416,"Width":328,"Height":722},"AlarmFlags":6,"MatchedFtVersion":1513229032,"OverMaxCount":false,"AppearCnt":0,"StartTime":1729506031,"EndTime":1729506041,"Similarity":0.0,"SnapId":3043,"SnapChn":9,"SnapFtVersion":12591105,"Gender":1,"SnapAge":-1,"SnapAgeGrp":3,"Expression":-1,"Hair":2,"Hat":1,"GlassType":1,"MouthMask":1,"Mustache":1,"GrpEnableAlarm":true}]},{"time":"10/21/2024 10:20:42","channel_alarm":[{"channel":"CH1","record_flag":{"s":"G"}},{"channel":"CH2","record_flag":{}},{"channel":"CH3","record_flag":{}},{"channel":"CH4","record_flag":{"s":"R","r":"SR"}},{"channel":"CH5","record_flag":{}},{"channel":"CH6","record_flag":{"s":"R","r":"SR"}},{"channel":"CH7","record_flag":{}},{"channel":"CH8","record_flag":{}},{"channel":"CH9","record_flag":{"s":"R","r":"SR"}},{"channel":"CH10","record_flag":{"s":"R","r":"SR"}},{"channel":"CH11","record_flag":{}},{"channel":"CH12","record_flag":{}},{"channel":"CH13","record_flag":{}},{"channel":"CH14","record_flag":{}},{"channel":"CH15","record_flag":{}},{"channel":"CH16","record_flag":{}}]},{"time":"10/21/2024 10:20:43","channel_alarm":[{"channel":"CH1","record_flag":{"s":"G"}},{"channel":"CH2","record_flag":{}},{"channel":"CH3","record_flag":{}},{"channel":"CH4","record_flag":{"s":"R","r":"SR"}},{"channel":"CH5","record_flag":{}},{"channel":"CH6","record_flag":{"s":"R","r":"SR"}},{"channel":"CH7","record_flag":{}},{"channel":"CH8","record_flag":{}},{"channel":"CH9","record_flag":{"s":"R","r":"SR"}},{"channel":"CH10","record_flag":{"s":"R","r":"SR"}},{"channel":"CH11","record_flag":{}},{"channel":"CH12","record_flag":{}},{"channel":"CH13","record_flag":{}},{"channel":"CH14","record_flag":{}},{"channel":"CH15","record_flag":{}},{"channel":"CH16","record_flag":{}}]}],"reader_id":7,"sequence":492,"lap_number":7,"update_feature":false}}'

    result = json.loads(response)
    if result is not None and result.get("result") == 'success':
        data = result.get("data")
        check(data)
        print("success")



