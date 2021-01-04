#!/usr/bin/env python
"""
 Created by howie.hu at 2018/10/17.
 这是为了方便请求构造的代理池服务 各位读者可忽略
"""

from ruia import Middleware, Request

se_middleware = Middleware()


@se_middleware.request
async def add_random_proxy(request):
    request.kwargs.update({"proxy": await update_proxy()})
    request.request_config.update({"RETRY_FUNC": retry_func})


async def update_proxy():
    proxy = await get_proxy_ip()
    if proxy:
        proxy = "http://" + proxy
    else:
        proxy = None
    return proxy


async def retry_func(request):
    proxy = await update_proxy()
    request.kwargs.update({"proxy": proxy})
    return request


async def get_proxy_ip(valid: int = 1) -> str:
    """
    ip 代理池函数
    :param valid:
    :return:
    """
    proxy_server = "http://0.0.0.0:8002"
    kwargs = {
        "json": {
            # pass
        }
    }
    res = await Request(
        url=proxy_server, method="POST", res_type="json", **kwargs
    ).fetch()
    proxy = ""
    if res.status == 200:
        proxy = res.html.get("info").get("proxy")
    return proxy
