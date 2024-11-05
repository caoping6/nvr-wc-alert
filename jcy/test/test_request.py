import requests

seq = 2

def params():
    sequence = seq if seq > 0 else 3
    print(sequence)

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
    params()
    print(seq)