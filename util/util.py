import logging
import json
import os
from logging.handlers import TimedRotatingFileHandler


def validator(config: dict) -> bool:
    """
    验证 config.json 是否缺少字段
    :param config: config.json's content
    :return: True or Exception
    :except ValueError: field is required but not contains
    :except KeyError: "carrier" is illegal
    """
    for key in ['username', 'password', 'carrier']:
        if not config.__contains__(key):
            raise KeyError('field "{}" is required in config.json'.format(key))

    if config['carrier'] not in ['default', 'unicom', 'cmcc', 'ctcc', 'local']:
        raise ValueError('value of "carrier" should be one of ["default", "unicom", "cmcc", "ctcc", "local"], '
                         'but "{}" is given'.format(config['carrier']))

    return True


def config_loader(config_file_name: str = 'config.json') -> dict:
    """
    从 config.json 中加载配置
    :return: KV 字典
    """
    config_path = get_config_file_path(config_file_name=config_file_name)
    if not os.path.exists(config_path):
        raise FileNotFoundError('{} not found'.format(config_path))
    else:
        with open(get_config_file_path(config_file_name=config_file_name)) as file:
            config = json.load(file)
            if validator(config):
                return config

    raise Exception('Unexpected execution')


def get_config_file_path(config_file_name: str = 'config.json', absolute: bool = False) -> str:  # 返回账号密码的存储路径
    """
    得到 config.json 的绝对路径
    :param config_file_name: config 文件名，默认为 config.json
    :param absolute: 如果为 True，就是 UPCNet 目录下的 config.json，否则就是运行目录下的 config.json
    :return: config.json 的绝对路径
    """
    if absolute:
        path = os.path.split(os.path.realpath(__file__))[0]  # 脚本根目录
        return os.path.join(path, config_file_name)

    return os.path.join(os.getcwd(), config_file_name)


