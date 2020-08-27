from __future__ import absolute_import, print_function

import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        from util import get_logger
        import time
        logger = get_logger('S', interval=3, backup_count=3)

        for i in range(9):
            logger.info(i)
            time.sleep(1)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
