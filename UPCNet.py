import typing
import logging
from upcnet import config_loader, login as _login, get_logger, skip_online

logger: logging.Logger = get_logger('D')


@skip_online(print_function=logger.info)
def login():
    config: typing.Dict[str, str] = config_loader()
    _login(config=config, print_function=logger.info)


def main():
    login()


if __name__ == '__main__':
    main()
