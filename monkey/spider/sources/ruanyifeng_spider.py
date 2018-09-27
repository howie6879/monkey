#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/27.
 Target: http://www.ruanyifeng.com/blog/archives.html
"""

from aspider import AttrField, Item, Request, Spider, TextField
from aspider_ua import middleware

from monkey.database.motor_base import MotorBase


class ArchivesItem(Item):
    """
    eg: http://www.ruanyifeng.com/blog/archives.html
    """
    target_item = TextField(css_select='div#beta-inner li.module-list-item')
    href = AttrField(css_select='li.module-list-item>a', attr='href')


class ArticleListItem(Item):
    """
    eg: http://www.ruanyifeng.com/blog/essays/
    """
    target_item = TextField(css_select='div#alpha-inner li.module-list-item')
    title = TextField(css_select='li.module-list-item>a')
    href = AttrField(css_select='li.module-list-item>a', attr='href')


class BlogSpider(Spider):
    """
    针对博客源 http://www.ruanyifeng.com/blog/archives.html 的爬虫
    这里为了模拟ua，引入了一个aspider的第三方扩展
        - aspider-ua: https://github.com/howie6879/aspider-ua
        - pipenv install aspider-ua
        - 此扩展会自动为每一次请求随机添加 User-Agent
    """
    # 设置启动URL
    start_urls = ['http://www.ruanyifeng.com/blog/archives.html']
    # 爬虫模拟请求的配置参数
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    # 请求信号量
    concurrency = 10
    blog_nums = 0

    async def parse(self, res):
        items = await ArchivesItem.get_items(html=res.html)
        try:
            self.mongo_db = MotorBase(loop=self.loop).get_db()
        except Exception as e:
            self.logger.exception(e)
        for item in items:
            yield Request(
                item.href,
                callback=self.parse_item,
                request_config=self.request_config,
            )

    async def parse_item(self, res):
        items = await ArticleListItem.get_items(html=res.html)
        for item in items:
            # 已经抓取的链接不再请求
            is_exist = await self.mongo_db.docs.find_one({'url': item.href}) or {}

            if not is_exist.get('html'):
                yield Request(
                    item.href,
                    callback=self.save,
                    metadata={'title': item.title},
                    request_config=self.request_config,
                )

    async def save(self, res):
        # 好像有两个url一样 原本的博客总数1725 在入库后变成了1723
        data = {
            'url': res.url,
            'title': res.metadata['title'],
            'html': res.html
        }

        try:
            await self.mongo_db.docs.update_one({
                'url': data['url']},
                {'$set': data},
                upsert=True)
        except Exception as e:
            self.logger.exception(e)


def main():
    BlogSpider.start(middleware=middleware)


if __name__ == '__main__':
    main()
