import json

import requests
import time
import threading
from urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPDigestAuth
from read_config import ReadConfig
from logger_util import Logger

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = Logger()


class Heartbeat:
    login_dict = ReadConfig("login", 'jcy/conf/alert.conf').get_config()
    _host = login_dict['host']
    _username = login_dict['username']
    _password = login_dict['password']
    _heart_url = _host + "/API/Login/Heartbeat"
    _login_url = _host + "/API/Web/Login"
    _check_url = _host + "/API/Event/Check"
    _instance = None
    _token = None
    _cookie = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Heartbeat, cls).__new__(cls)
                    # cls._instance.login()
        return cls._instance

    def login(self, algorithm='SHA-256'):

        response = requests.post(self._login_url, auth=HTTPDigestAuth(self._username, self._password), verify=False)

        # 检查是否需要重新认证
        if response.status_code == 401:
            # 如果提供的算法不是服务器支持的算法，则可能需要调整算法
            response.request.headers['Authorization'] = 'Digest ' + algorithm
            # 重新发送请求
            response = requests.get(self._login_url, auth=HTTPDigestAuth(self._username, self._password), verify=False)

        # 检查登录是否成功
        if response.ok:
            self._token = response.headers.get('X-csrftoken')
            self._cookie = response.headers.get('Set-Cookie')

            logger.info('token:' + self._token)
            logger.info(f"login token: {self._token} ;login Cookie: {self._cookie}")

            print('Cookie:' + response.headers.get('Set-cookie'))

        else:
            print('登录失败')

    # 定义请求函数
    def send_heartbeat(self):
        logger.info("start heartbeat")

        headers = {
            'Content-Type': 'application/json',
            'X-csrftoken': self._token,
            'Cookie': self._cookie
        }

        try:
            response = requests.post(self._heart_url, headers=headers, verify=False, json={})
            result = json.loads(response.text)
            logger.info(f"Heartbeat Status Code: {response.status_code}\nResponse Text: {response.text}")
            if 'error_code' in result:
                self.login()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            self.login()

    def check(self, data):
        logger.debug("start check")
        headers = {
            'Content-Type': 'application/json',
            'X-csrftoken': self._token,
            'Cookie': self._cookie
        }
        try:
            response = requests.post(self._check_url, headers=headers, verify=False, json=data)
            logger.debug(f"Check Status Code: {response.status_code}")
            if response.status_code != 200:
                logger.info(f"Check Response and retry one times: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Check Request failed: {e}")
            self.login()


if __name__ == '__main__':

    hb = Heartbeat()

    print("token=" + hb._token)
    print("cookie=" + hb._cookie)
    while True:
        # 运行所有调度任务
        logger.info("Heartbeat loop")
        time.sleep(10)
        hb.send_heartbeat()
