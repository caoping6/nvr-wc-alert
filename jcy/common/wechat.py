# -*- coding: utf-8 -*-

import json

import requests
import threading
from datetime import datetime, time
from read_config import ReadConfig

from logger_util import Logger

logger = Logger()


class WeChatClient:
    weixin_dict = ReadConfig("weixin", 'jcy/conf/alert.conf').get_config()
    openid_dict = ReadConfig("jcy", 'jcy/conf/openid.conf').get_config()

    _host = weixin_dict['host']
    _appid = weixin_dict['appid']
    _secret = weixin_dict['secret']
    _template_id = weixin_dict['template_id']
    _title= weixin_dict['title']
    _access_token = None
    _token_url = _host + "/cgi-bin/token?grant_type=client_credential&appid=" + _appid + "&secret=" + _secret
    _send_url = _host + "/cgi-bin/message/template/send?access_token="
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(WeChatClient, cls).__new__(cls)
                    cls._instance.get_token()
        return cls._instance

    def get_token(self):
        response = requests.get(self._token_url)
        logger.info(f"get weixin token: {response.status_code} ;text: {response.text}")

        # 检查登录是否成功
        if response.ok:
            res = json.loads(response.text)
            if 'access_token' in res:
                self._access_token = res.get('access_token')
        else:
            logger.error('获取access token失败')

    # 定义请求函数
    def send_msg(self, phone, name, alert_time):
        url = self._send_url + self._access_token
        # 格式化日期和时间为字符串
        formatted_time = alert_time.strftime("%Y-%m-%d %H:%M:%S")
        open_id = self.openid_dict[phone]
        data = {
            "touser": open_id,
            "template_id": self._template_id,
            "data": {

                "thing1": {
                    "value": self._title
                },
                "time4": {
                    "value": formatted_time
                },
                "thing2": {
                    "value": name
                }
            }
        }
        try:

            response = requests.post(url, json=data)
            logger.info(f"send msg status code: {response.status_code}; Response Text: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")


if __name__ == '__main__':
    web_client = WeChatClient()
    # web_client.get_token()
    # print(web_client._access_token)
    # web_client.send_msg('17611225585', '曹平', datetime.now())
    openid = web_client.openid_dict.get("曹平")
    print(openid)
    if openid is None:
        print("ssss")

