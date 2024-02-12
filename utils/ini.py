import configparser
import logging
import os.path

from utils import env

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s]- %(levelname)s - %(message)s')

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 获取配置文件中的配置项的值
def get_property(config_name, section, property_name):
    config = configparser.ConfigParser()
    config_path = os.path.join(root_path, "config", f'{config_name}.ini')
    config.read(config_path, encoding="utf-8")
    try:
        return config.get(section, property_name)
    except Exception as e:
        logging.error("获取配置信息字符串出错，错误信息为：{}".format(e))
        return None