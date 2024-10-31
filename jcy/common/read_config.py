import configparser
import os
from jcy.common.logger_util import Logger
logger = Logger()

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
logger.info("config parser BASEDIR=" + BASEDIR)


class ReadConfig(object):
    _config = None

    def __init__(self, section, config):
        """
        init conf
        :param section: section
        :param config: config file
        """
        conf_path = os.path.join(BASEDIR, config)

        self._config = self.__init_config(section, conf_path)

    def __init_config(self, section, config):
        config_dict = dict()
        config_parser = configparser.ConfigParser()
        config_parser.read(config, encoding="utf8")
        if config_parser.has_section(section):
            config_dict = dict(config_parser.items(section))
        return config_dict

    def get_config(self):
        return self._config


if __name__ == '__main__':
    config_dict = ReadConfig("login", 'jcy/conf/alert.conf')
    logger.info("name=" + config_dict.get_config().get("username"))
