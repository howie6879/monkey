#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/1.
"""
from sanic import Sanic

from aiocache import SimpleMemoryCache

from monkey.config import Config
from monkey.database.motor_base import MotorBase
from monkey.views.bp_home import bp_home

app = Sanic(__name__)
app.blueprint(bp_home)


@app.listener('before_server_start')
def init_cache(app, loop):
    """
    初始化操作 对一些参数进行配置
    :param app:
    :param loop:
    :return:
    """
    app.config['monkey_config'] = Config
    app.cache = SimpleMemoryCache()
    app.mongo_db = MotorBase(loop=loop).get_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", workers=2, port=8001, debug=False)
