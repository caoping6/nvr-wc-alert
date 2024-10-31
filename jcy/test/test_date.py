from datetime import datetime,  time
import time
from jcy.common.read_config import ReadConfig
from jcy.common.logger_util import Logger
logger = Logger("../logs/test.log")

clock_dict = ReadConfig("clock_time", 'jcy/conf/alert.conf').get_config()


if __name__ == '__main__':


    # 运行 while 循环
    while True:
        # 获取当前时间和开始时间之间的差值
        elapsed_time = time.time() - start_time

        # 打印经过的时间（可选）
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")

        # 检查是否已经超过30秒
        if elapsed_time > 30:
            print("Exiting loop after 30 seconds.")
            break

        # 为了减少CPU占用率，可以添加一点延迟
        time.sleep(1)



