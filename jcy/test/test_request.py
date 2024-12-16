import requests
from jcy.common.logger_util import Logger
import json
logger = Logger("../logs/test.log")

seq = 2

def params():
    sequence = seq if seq > 0 else 3
    print(sequence)

def change():
    global seq
    seq=10

if __name__ == '__main__':
    # response = requests.request(
    #     method='GET',
    #     url='http://ta-test.aidoutang.com/haichuan/api/ai/getStuAndLearningInfo',
    #     params={
    #         "stu_ids": "75669051",
    #         "teacher_id": 1094418,
    #         # "work_code": "W001234",
    #         "brand": 100
    #     }
    # )
    #
    # print(response)
    # data = {'name': 'Alice', 'age': 30, 'city': 'New York'}
    # print(json.dumps(data))
    # 定义两个变量
    sequence = 10
    face_sequence = 15

    # 使用条件表达式实现三元运算符的功能
    result = sequence if sequence > face_sequence else face_sequence

    print(result)  # 输出: 10