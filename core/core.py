import typing
import requests
from urllib.parse import quote, urlparse


def skip_online(print_function=print):
    """
    如果有网络就跳过
    :param print_function: 输出流
    :return: None
    """
    def decorate(func):
        def execute(*args, **kwargs) -> typing.Any:
            if is_online():
                print_function('Currently Online')
                return None
            else:
                return func(*args, **kwargs)

        return execute

    return decorate


def carrier_choose(carrier: str):  # 运营商选择
    if carrier == '1':
        return 'default'  # 校园网
    elif carrier == '2':
        return 'unicom'  # 联通
    elif carrier == '3':
        return 'cmcc'  # 移动
    elif carrier == '4':
        return 'ctcc'  # 电信
    return 'local'  # 校园内网


def is_online():
    """
    判断当前是否有网络
    :return: True or False
    """
    try:
        url = requests.get('http://captive.lucien.ink', allow_redirects=True, timeout=3).url
    except:
        return False
    if ~url.find('https://www.lucien.ink'):
        return True
    return False


def logout():
    """
    登出
    :return: None
    """
    def out(address):
        url = requests.get(address, allow_redirects=True, timeout=3).url
        if ~url.find('userIndex='):
            user_index = url[url.find('userIndex=') + 10:]
            requests.post(address + '/eportal/InterFace.do?method=logout', data={'userIndex': user_index})

    try:
        out('http://lan.upc.edu.cn')

    except:
        print('Logout failed')

    else:
        if is_online():
            print('Logout failed')
        else:
            print('Logout success')


def login(config: dict, print_function=print):
    """
    登陆
    :param config: 配置
    :param print_function: 输出流
    :return:
    """
    address = 'http://121.251.251.217'
    magic_word = '/&userlocation=ethtrunk/62:3501.0'
    lan_special_domain = 'http://lan.upc.edu.cn'
    login_parameter = '/eportal/InterFace.do?method=login'
    try:
        true_text = requests.get(address + magic_word, allow_redirects=True).text
        true_url = requests.post(address + magic_word, allow_redirects=True).url
        url = lan_special_domain + login_parameter
        if true_text.find('Error report') > -1:
            true_url = requests.post('http://121.251.251.207' + magic_word, allow_redirects=True).url  # 特殊处理
            url = address + login_parameter
        arg_parsed = quote(urlparse(true_url).query)

        if arg_parsed.find('wlanuserip') == -1:
            print_function('Currently online')

        else:
            payload = {'userId': config['username'],
                       'password': config['password'],
                       'service': config['carrier'],
                       'queryString': arg_parsed,
                       'operatorPwd': '',
                       'operatorUserId': '',
                       'vaildcode': '',
                       'passwordEncrypt': 'false'}

            post_message = requests.post(url, data=payload)
            if post_message.text.find('success') >= 0:
                print_function('{} Login Success'.format(config['username']))
            else:
                print_function('Login Failed')
    except requests.exceptions.ConnectionError:
        print_function('Network Error')
