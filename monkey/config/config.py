#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/27.
"""

import os


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    MONGODB = dict(
        MONGO_HOST=os.getenv('MONGO_HOST', ""),
        MONGO_PORT=int(os.getenv('MONGO_PORT', 27017)),
        MONGO_USERNAME=os.getenv('MONGO_USERNAME', ""),
        MONGO_PASSWORD=os.getenv('MONGO_PASSWORD', ""),
        DATABASE='monkey',
    )
