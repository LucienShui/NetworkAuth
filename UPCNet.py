#!/usr/bin/python3
#!coding=utf-8
import urllib
import base64
import time
import os
import requests
import sys


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


def autoexit():  # 延时一秒后结束程序
    time.sleep(1)
    sys.exit()


def getpath():  # 返回账号密码的存储路径
    path = os.path.split(os.path.realpath(__file__))[0]  # 脚本根目录
    return "%s%sconfig.ini" % (path, os.path.sep)


def config_init():
    file_path = getpath()
    if not os.path.exists(file_path):
        str_tmp = input('School number: ')
        str_tmp = str_tmp + ' ' + input('Password: ')
        str_tmp = str_tmp + ' ' + input('1.default\n2.unicom\n3.cmcc\n4.ctcc\n5.local\nCommunications number: ')
        file = open(file_path, 'wb')
        file.write(encode(str_tmp))  # 加密后的字符串写入二进制文件


def online():
    try:
        url = requests.get("http://captive.lucien.ink", allow_redirects=True, timeout=3).url
    except:
        return False  # 超时，当前无外网
    if ~url.find("https://www.lucien.ink"):
        return True  # 当前有外网
    return False


def out(address):
    url = requests.get(address, allow_redirects=True, timeout=3).url
    if ~url.find("userIndex="):
        userIndex = url[url.find("userIndex=") + 10:]
        requests.post(address + "/eportal/InterFace.do?method=logout", data={'userIndex': userIndex})


def logout():
    try:
        out("http://lan.upc.edu.cn")

    except:
        print("Logout failed")

    else:
        if online():
            print("Logout failed")
        else:
            print("Logout success")


def login():
    url = ""
    argParsed = ""
    address = "http://121.251.251.217"
    magic_word = "/&userlocation=ethtrunk/62:3501.0"
    lan_special_domain = "http://lan.upc.edu.cn"
    login_parameter = "/eportal/InterFace.do?method=login"
    try:
        trueText = requests.get(address + magic_word, allow_redirects=True).text
        trueUrl = requests.post(address + magic_word, allow_redirects=True).url
        url = lan_special_domain + login_parameter
        if trueText.find("Error report") > -1:
            trueUrl = requests.post("http://121.251.251.207" + magic_word, allow_redirects=True).url  # 特殊处理
            url = address + login_parameter
        argParsed = urllib.parse.quote(urllib.parse.urlparse(trueUrl).query)
        if argParsed.find('wlanuserip') == -1:
            print("Currently online")
            autoexit()
    except requests.exceptions.ConnectionError:
        print("Network Error")
        autoexit()

    buf = decode(open(getpath(), "rb").readline())  # 读取二进制文件并解密
    payload = {'userId': buf.split(' ')[0],
               'password': buf.split(' ')[1],
               'service': service_choose(buf.split(' ')[2]),
               'queryString': argParsed,
               'operatorPwd': '',
               'operatorUserId': '',
               'vaildcode': '',
               'passwordEncrypt': 'false'}
    postMessage = requests.post(url, data=payload)
    if postMessage.text.find("success") >= 0:
        print("Login Success")
    else:
        print("Login Failed")
        autoexit()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            print('Too many args')

        else:
            argv = sys.argv[1]
            if argv == 'reset':
                file_path = getpath()
                if os.path.exists(file_path):
                    os.remove(file_path)
                print('Reset Success')

            elif argv == 'logout':
                logout()

            else:
                print('Wrong args')

    else:
        config_init()
        login()

    autoexit()
