import typing
import logging
from core import login as _login, skip_online
from util import config_loader, get_logger

logger: logging.Logger = get_logger('D')


@skip_online(print_function=logger.info)
def login(config: dict):
    _login(config=config, print_function=logger.info)


def main():
    try:
        config: typing.Dict[str, str] = config_loader()
    except (ValueError, FileNotFoundError) as e:
        logger.error(e)
    else:
        login(config=config)


if __name__ == '__main__':
    main()
