from __future__ import unicode_literals
from scrapy.spiders import CrawlSpider
from news.common.logger import Logger
from news.common import core_redis
from bs4 import BeautifulSoup
from news import settings
import requests
import random
import time
import os


class Basic_Spider(CrawlSpider):

    def __init__(self, redis_db=4, kind='fix', *args, **kwargs):
        settings.REDIS_DB = redis_db
        self.kind = kind
        self.set_log_path()
        self.is_all = 1 if kind == 'all' else 0
        self.log = Logger(settings.LOG_FILE)
        self.pid = os.getpid()

        self.header = {#'User-Agent': settings.USER_AGENT,
                       'Connection': 'keep-alive',
                       'Accept': 'application/json, text/plain, */*'}

        # core_redis.set_pid(self.kind, self.name, self.pid)

        super(Basic_Spider, self).__init__(*args, **kwargs)


    def get_redis_data(self, key, condition):
        return core_redis.get_redis_data(key, self.log,condition)

    def is_wrong_name(self, qymc, qymc_in_db, list_id, item_obj):
        '''
        如果企业名称和数据库中的名称不一样，就修改这条的标记位，不采了
        :param qymc:
        :param name_in_db:
        :param list_id:

        :return:
        '''
        res = {}
        res['item'] = item_obj
        if qymc == "":
            item_obj['table'] = self.name + '_list' if self.is_all == 1 else 'gs_list_fix'
            item_obj['flag'] = 2
            item_obj['list_id'] = list_id
            res['status'] = 1
        else:
            res['status'] = 0

        return res

    def set_log_path(self):
        types = self.name
        real_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", '/') + "/log/"
        log_path = real_path + types + '_' + str(random.random() * 10000)[:3] + '_' + time.strftime("%Y-%m-%d", time.localtime()) + ".log"
        settings.LOG_FILE = log_path
        return

    def add_del_pid(self, name):
        print ("name in Basic_spider.add_del_pid:"+name)
        core_redis.add_del_pid(self.is_all, name, self.pid)

    def get_html(self, url, method, data=None, parmas=None, headers=None, cookies=None, proxies=None):
        time.sleep(random.randint(3,6))
        method = requests.get if method == 'GET' else requests.post
        if headers is None:
            headers = self.header
        for _ in range(10):
            try:
                res = method(url, headers=headers, params=parmas, data=data, cookies=cookies, proxies=proxies)
                # res = method(url, headers=headers, params=parmas, data=data, cookies=cookies)

                if res.status_code == 200:
                    break
                time.sleep(3)
            except requests.exceptions.RequestException as e:
                print (e)

            res = None

        try:
            html = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')
        except Exception:
            html = None
            self.log.error("html解析失败...")

        return html