from __future__ import absolute_import, print_function

import logging
import os
from logging.handlers import TimedRotatingFileHandler


def get_logger(when: str = 'D', interval: int = 1, backup_count: int = 3) -> logging.Logger:
    """
        Get logger
        :param when:
            Calculate the real rollover interval, which is just the number of
            seconds between rollovers.  Also set the filename suffix used when
            a rollover occurs.  Current 'when' events supported:
            S - Seconds
            M - Minutes
            H - Hours
            D - Days

            Case of the 'when' specifier is not important; lower or upper case
            will work.
        :param interval:
        :param backup_count:
        :return:
        """
    log_dir = 'logs'
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter('%(asctime)s\t%(filename)s:%(lineno)s\t[%(levelname)-6s]\t%(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    timed_rotating_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, 'app.log'),
        when=when,
        interval=interval,
        backupCount=backup_count,
    )

    timed_rotating_file_handler.setFormatter(formatter)

    logging.basicConfig()

    logger = logging.getLogger('UPCNet')
    logger.setLevel(logging.INFO)

    logger.addHandler(timed_rotating_file_handler)

    return logger
