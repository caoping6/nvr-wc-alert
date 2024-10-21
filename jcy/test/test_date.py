import time
from datetime import datetime,  time
from jcy.common.read_config import ReadConfig
from jcy.common.logger_util import Logger
logger = Logger("../logs/test.log")

clock_dict = ReadConfig("clock_time", 'jcy/conf/alert.conf').get_config()


if __name__ == '__main__':
    morning_clock_in = clock_dict['morning_clock_in']
    print(morning_clock_in)



