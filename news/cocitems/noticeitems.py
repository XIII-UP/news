#-*- coding:UTF-8 -*-
from __future__ import unicode_literals
import scrapy


class NoticeNewsItem(scrapy.Item):
    title = scrapy.Field()  # 公司列表id
    url = scrapy.Field()  # 公路市场id

