import requests
from requests.auth import HTTPDigestAuth
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def login(username, password, url, algorithm='SHA-256'):
    response = requests.post(url, auth=HTTPDigestAuth(username, password), verify=False)

    print("request done....")
    print(response.text)

    # 检查是否需要重新认证
    if response.status_code == 401:
        # 如果提供的算法不是服务器支持的算法，则可能需要调整算法
        response.request.headers['Authorization'] = 'Digest ' + algorithm
        # 重新发送请求
        response = requests.get(url, auth=HTTPDigestAuth(username, password), verify=False)

    # 检查登录是否成功
    if response.ok:
        print('登录成功')
        print('token:' + response.headers.get('X-csrftoken'))
        print('Cookie:' + response.headers.get('Set-cookie'))
    else:
        print('登录失败')

    return response


# 使用示例
print("start....")
login('admin', 'shuaiCAI2@', 'https://192.168.1.52:443/API/Web/Login')
