#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/27.
"""
import os
import sys
import time

from importlib import import_module

sys.path.append('./')

from monkey.config import Config
from monkey.utils.log import logger


def file_name(file_dir=os.path.join(Config.BASE_DIR, 'spider/sources')):
    """
    Get spider class
    :param file_dir:
    :return:
    """
    all_files = []
    for file in os.listdir(file_dir):
        if file.endswith('_spider.py'):
            all_files.append(file.replace('.py', ''))
    return all_files


def spider_console():
    start = time.time()
    all_files = file_name()
    for spider in all_files:
        spider_module = import_module(
            "monkey.spider.sources.{}".format(spider))
        spider_module.main()

    logger.info(f"Time costs: {time.time() - start}")


if __name__ == '__main__':
    spider_console()
