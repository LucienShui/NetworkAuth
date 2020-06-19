#!/usr/bin/python3
# !coding=utf-8
import base64
import typing
import json
import time
import os
import requests
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from urllib.parse import quote, urlparse


def skip_online(func):
    def execute(*args, **kwargs) -> typing.Any:
        if is_online():
            return None
        else:
            return func(*args, **kwargs)
    return execute


def service_choose(service):  # 运营商选择
    if service == '1':
        return "default"  # 校园网
    elif service == '2':
        return "unicom"  # 联通
    elif service == '3':
        return "cmcc"  # 移动
    elif service == '4':
        return "ctcc"  # 电信
    return "local"  # 校园内网


def encode(string):  # 加密
    return base64.encodebytes(str.encode(string, 'utf-8'))


def decode(code):  # 解密
    return bytes.decode(base64.decodebytes(code), 'utf-8')


def auto_exit():  # 延时一秒后结束程序
    time.sleep(1)
    sys.exit()


def get_config_file_path(absolute: bool = False) -> str:  # 返回账号密码的存储路径
    if absolute:
        path = os.path.split(os.path.realpath(__file__))[0]  # 脚本根目录
        return "%s%sconfig.ini" % (path, os.path.sep)
    return 'config.ini'


def config_loader() -> dict:
    file_path = get_config_file_path()
    if not os.path.exists(file_path):
        config: typing.Dict[str, str] = dict()
        config['username']: str = input('School number: ')
        config['password']: str = input('Password: ')
        config['service_name']: str = input('1.default\n2.unicom\n3.cmcc\n4.ctcc\n5.local\nCommunications number: ')
        file = open(file_path, 'wb')
        file.write(encode(json.dumps(config)))  # 加密后的字符串写入二进制文件
        return config
    else:
        json_str = decode(open(get_config_file_path(), "rb").read())  # 读取二进制文件并解密
        return json.loads(json_str)


def is_online():
    try:
        url = requests.get("http://captive.lucien.ink", allow_redirects=True, timeout=3).url
    except:
        return False  # 超时，当前无外网
    if ~url.find("https://www.lucien.ink"):
        return True  # 当前有外网
    return False


def logout():
    def out(address):
        url = requests.get(address, allow_redirects=True, timeout=3).url
        if ~url.find("userIndex="):
            user_index = url[url.find("userIndex=") + 10:]
            requests.post(address + "/eportal/InterFace.do?method=logout", data={'userIndex': user_index})

    try:
        out("http://lan.upc.edu.cn")

    except:
        print("Logout failed")

    else:
        if is_online():
            print("Logout failed")
        else:
            print("Logout success")


def login(config: dict, print_function=print):
    address = "http://121.251.251.217"
    magic_word = "/&userlocation=ethtrunk/62:3501.0"
    lan_special_domain = "http://lan.upc.edu.cn"
    login_parameter = "/eportal/InterFace.do?method=login"
    try:
        true_text = requests.get(address + magic_word, allow_redirects=True).text
        true_url = requests.post(address + magic_word, allow_redirects=True).url
        url = lan_special_domain + login_parameter
        if true_text.find("Error report") > -1:
            true_url = requests.post("http://121.251.251.207" + magic_word, allow_redirects=True).url  # 特殊处理
            url = address + login_parameter
        arg_parsed = quote(urlparse(true_url).query)

        if arg_parsed.find('wlanuserip') == -1:
            print_function("Currently online")

        else:
            payload = {'userId': config['username'],
                       'password': config['password'],
                       'service': service_choose(config['service_name']),
                       'queryString': arg_parsed,
                       'operatorPwd': '',
                       'operatorUserId': '',
                       'vaildcode': '',
                       'passwordEncrypt': 'false'}

            post_message = requests.post(url, data=payload)
            if post_message.text.find("success") >= 0:
                print_function("{} Login Success".format(config['username']))
            else:
                print_function("Login Failed")
    except requests.exceptions.ConnectionError:
        print_function("Network Error")


def get_logger() -> logging.Logger:
    log_dir = 'logs'
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig()

    logger = logging.getLogger('UPCNet')
    logger.setLevel(logging.INFO)
    timed_rotating_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, 'log.txt'),
        when='D',
        interval=1,
        backupCount=3,
    )

    formatter = logging.Formatter('%(asctime)s [%(levelname)-5s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    timed_rotating_file_handler.setFormatter(formatter)
    logger.addHandler(timed_rotating_file_handler)

    return logger


def main():
    if len(sys.argv) > 1:
        if len(sys.argv) > 3:
            print('Too many args')
            auto_exit()

        if len(sys.argv) == 3:

            logger: logging.Logger = get_logger()

            if sys.argv[1] == 'up' and sys.argv[2] == '-d':
                config = config_loader()
                while True:
                    try:
                        login(config=config, print_function=logger.info)
                    except:
                        pass
                    time.sleep(10)

        else:
            argv = sys.argv[1]
            if argv == 'reset':
                file_path = get_config_file_path()
                if os.path.exists(file_path):
                    os.remove(file_path)
                print('Reset Success')

            elif argv == 'logout':
                logout()

            else:
                print('Wrong args')

    else:
        config = config_loader()
        logger: logging.Logger = get_logger()
        login(config=config, print_function=logger.info)

    auto_exit()


if __name__ == '__main__':
    main()
