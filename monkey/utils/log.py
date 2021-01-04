#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/27.
"""

import logging

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(format=logging_format, level=logging.DEBUG)
logger = logging.getLogger()
