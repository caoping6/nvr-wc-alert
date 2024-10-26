import loguru
import uuid
import threading
import sys
from enum import Enum

class LogLevel(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Logger:
    _instance = None
    _lock = threading.Lock()
    _log_file = None
    _log_handler = None
    _console_handler = None

    def __new__(cls, *args, **kwargs):
        cls._log_file = "logs/app.log"
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
                    if args.__len__() > 0:
                        cls._log_file = args[0]
                    cls._instance._setup_logger()
                    cls._instance.initialize()
        return cls._instance

    def _setup_logger(self):
        # 设置日志记录器
        self.logger = loguru.logger
        self.logger.remove()  # 移除默认的日志处理器
        # self.logger.add(sys.stderr, format=self._get_log_format(), colorize=True)
        # self.logger.add(self._log_file, format=self._get_log_format(), rotation="10 MB")
        self.set_custom_logger(write_level='INFO')
        self.set_console_logger(console_level="INFO")
        self.traceid_dict = {}  # 初始化 traceid 字典

    def _get_log_format(self):
        return (
            "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>] "
            "[<level>{level}</level>] "
            "[<cyan>{file}:{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>] "
            "<red>{message}</red> | "
            "<blue>{extra}</blue>"
        )

    def set_custom_logger(self, write_level='DEBUG'):
        write_log_level_list = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if write_level.upper() not in write_log_level_list:
            raise Exception(f'写入log设置的等级不存在,写入log等级为:{write_log_level_list}')
        # 记录设置writer_level
        if self._log_handler is not None:
            self.logger.remove(self._log_handler)

        self._log_handler = self.logger.add(
            sink=self._log_file,  # 每次调用时都生成新的log文件
            rotation='2 MB',  # 超过50MB就会重新生产一个文件（常用），其他用法可以查一下
            encoding='utf-8',
            format=self._get_log_format(),
            level=write_level,
            enqueue=True,  # 开启异步
            # colorize=True,  # 开启颜色   开启颜色导致乱码
        )

    def set_console_logger(self, console_level='INFO'):

        console_log_level_list = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if console_level.upper() not in console_log_level_list:
            raise Exception(f'控制台log设置的等级不存在,控制台log等级为:{console_log_level_list}')
        if self._console_handler is not None:
            self.logger.remove(self._console_handler)

        # 控制台输出
        self._console_handler = self.logger.add(
            sink=sys.stdout,
            level=console_level,  # 设置log的level等级
            format=self._get_log_format(),
            colorize=True,  # 开启颜色
            enqueue=True,  # 开启异步
        )

    def update_traceid(self):
        self.set_traceid(str(uuid.uuid4()).replace("-", ""))

    def get_traceid(self):
        thread_id = threading.get_ident()
        return self.traceid_dict.get(thread_id, None)

    def set_traceid(self, traceid=None):
        if traceid is None:
            traceid = str(uuid.uuid4())
        thread_id = threading.get_ident()
        self.traceid_dict[thread_id] = traceid

    def initialize(self):
        self.set_traceid(str(uuid.uuid4()).replace("-", ""))

    def debug(self, message, **extra):
        message = f"[traceid:{self.get_traceid()}] - {message}"
        self.logger.opt(depth=1).log(LogLevel.DEBUG.value, message, **extra)

    def info(self, message, **extra):
        message = f"[traceid:{self.get_traceid()}] - {message}"
        self.logger.opt(depth=1).log(LogLevel.INFO.value, message, **extra)

    def warning(self, message, **extra):
        message = f"[traceid:{self.get_traceid()}] - {message}"
        self.logger.opt(depth=1).log(LogLevel.WARNING.value, message, **extra)

    def error(self, message, **extra):
        message = f"[traceid:{self.get_traceid()}] - {message}"
        self.logger.opt(depth=1).log(LogLevel.ERROR.value, message, **extra)
