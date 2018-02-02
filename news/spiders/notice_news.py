from __future__ import unicode_literals
from news.cocitems.noticeitems import NoticeNewsItem
from .Basic_Spider import Basic_Spider
from news import settings
from bs4 import BeautifulSoup
from scrapy import Request
import re

LIST_SUFFIX = settings.LIST_SUFFIX
FIX_LIST_TABLE = settings.TABLES['fix_company_table']


class NoticeNewsSpider(Basic_Spider):
    name = "notice_news"
    custom_settings = {
        'ITEM_PIPELINES': {'news.cocpipelines.noticepipelines.NoticePipeline': 1},
        'HTTPCACHE_ENABLED': True,
    }

    def __init__(self, *args, **kwargs):
        self.name = "notice_news"
        self.root_url = "http://www.mohurd.gov.cn/wjfb/index{i}.html"
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            # 'Connection': 'keep-alive',
            'Host': 'www.mohurd.gov.cn',
            'Upgrade-Insecure-Requests': '1',
        }

        super(NoticeNewsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(self.root_url.format(i=''), callback=self.parse)

    def parse(self, response):
        meta = {}
        try:
            pages = response.xpath("//span[contains(text(),'共')]/text()").extract()[0][1:-1]
        except IndexError:
            self.log.info('get pages failed...\n')
        else:
            for i in range(2, int(pages) + 1):
                url = self.root_url.format(i='_' + str(i))
                yield Request(
                    url,
                    callback=self.get_page,
                    headers=self.header,
                    dont_filter=False
                )
        finally:
            lists = response.xpath("//a[contains(@href,'http://www.mohurd.gov.cn/wjfb/2')]")
            for i in lists:
                meta['url'] = i.xpath('@href').extract()[0]
                tds = i.xpath('../following-sibling::*').xpath('string(.)').extract()
                meta['wjbh'] =tds[0].strip()
                meta['fbsj'] =tds[1].strip()
                yield Request(
                    meta['url'],
                    callback=self.new_content,
                    meta=meta,
                    headers=self.header,
                    dont_filter=False
                )

    def get_page(self, response):
        meta_dic = response.meta
        lists = response.xpath("//a[contains(@href,'http://www.mohurd.gov.cn/wjfb/2')]")
        for i in lists:
            meta_dic['url'] = i.xpath('@href').extract()[0]
            tds = i.xpath('../following-sibling::*').xpath('string(.)').extract()
            meta_dic['wjbh'] = tds[0].strip()
            meta_dic['fbsj'] = tds[1].strip()
            yield Request(
                meta_dic['url'],
                callback=self.new_content,
                meta=meta_dic,
                headers=self.header,
                dont_filter=False
            )

    def new_content(self, response):
        table = response.xpath("//div[@class='info']").extract()[0]

        print(table)

