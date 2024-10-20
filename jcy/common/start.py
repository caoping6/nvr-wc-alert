import requests
from heartbeat import Heartbeat
from read_config import ReadConfig
from wechat import WeChatClient
from logger_util import Logger
logger = Logger("alert.log")

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if __name__ == '__main__':
    # 获取当前日期和时间

    print("当前日期和时间:")

