#-*- coding:UTF-8 -*-
from __future__ import unicode_literals
from news import settings
from news.common.configsql import ConfigSql
from news.common.logger import Logger
import base64

# 代理服务器
proxyServer = "https://proxy.abuyun.com:9020"

# 隧道身份信息
proxyUser = settings.PROXY_USER
proxyPass = settings.PROXY_PASS
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

FIX_LIST_TABLE = settings.TABLES['fix_company_table']


class ProxyMiddleware(object):
    def __init__(self, auth_encoding='latin-1'):
        self.proxies = {}
        self.auth_encoding = auth_encoding
        self.proxies[proxyServer] = proxyUser + proxyPass
        # super(ProxyMiddleware, self).__init__()

    def process_request(self, request, spider):
        if 'jz' in spider.name:
            request.meta["proxy"] = proxyServer
            request.headers["Proxy-Authorization"] = proxyAuth

class AccessExceptionMiddleware(ConfigSql):
    """
    # 访问异常中间件
    """
    def __init__(self):
        super(AccessExceptionMiddleware, self).__init__()
        self.log = Logger()

    def process_response(self,request,response,spider):

        if request.url == request.meta.get('url'):
            table = (spider.name + settings.LIST_SUFFIX) if not request.meta['task_id'] else FIX_LIST_TABLE
            list_id = request.meta.get('list_id')
            if request.meta.get('gs_id') is None:
                self.change_flag(table, list_id)
            if request.meta.get('retry_times') >= 10:
                if int(response.status) >= 400:
                    self.log.info("access failed....\n")
                    self.change_flag(table, list_id)
                elif int(response.status) != 200:
                    self.change_flag(table, list_id, 3)
                    self.log.info( request.meta['name'] + "is not 200. It`s status is "+str(response.status))
        else:
            pass

        return response
