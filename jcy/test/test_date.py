import time
from datetime import datetime,  time
from jcy.common.read_config import ReadConfig
from jcy.common.logger_util import Logger
from jcy.common.wechat import WeChatClient

logger = Logger("../logs/test.log")

clock_dict = ReadConfig("clock_time", 'jcy/conf/alert.conf').get_config()

web_client = WeChatClient()

if __name__ == '__main__':
    morning_clock_in = clock_dict['morning_clock_in']
    print(morning_clock_in)



