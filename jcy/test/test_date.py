from datetime import datetime,  time
import time
from jcy.common.read_config import ReadConfig
from jcy.common.logger_util import Logger
from jcy.common.wechat import WeChatClient

logger = Logger("../logs/test.log")

clock_dict = ReadConfig("clock_time", 'jcy/conf/alert.conf').get_config()

web_client = WeChatClient()

if __name__ == '__main__':


    try:
        print(1/0)
    except Exception as e:
        logger.error(f"check first failed: {e}")


