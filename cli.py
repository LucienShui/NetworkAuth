#!/usr/bin/env python3
import sys
import logging
import os
import time
from core import login, logout
from util import get_logger, config_loader, get_config_file_path


def main():
    if len(sys.argv) > 1:
        if len(sys.argv) > 3:  # 大于两个参数
            print('Too many args')

        elif len(sys.argv) == 3:  # 刚好两个参数

            logger: logging.Logger = get_logger()

            if sys.argv[1] == 'up' and sys.argv[2] == '-d':
                config = config_loader()
                while True:
                    try:
                        login(config=config, print_function=logger.info)
                    except:
                        pass
                    time.sleep(10)

        else:  # 一个参数
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

    else:  # 没有参数
        config = config_loader()
        logger: logging.Logger = get_logger()
        login(config=config, print_function=logger.info)


if __name__ == '__main__':
    main()
