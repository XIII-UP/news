#-*- coding:UTF-8 -*-
from __future__ import unicode_literals
from news import settings
from news.cocitems import noticeitems
from news.common.collectsql import CollectSql
from news.common.configsql import ConfigSql
from news.common.logger import Logger
import json
import re

FIX_LIST_TABLE = settings.TABLES['fix_company_table']
LIST_SUFFIX = settings.LIST_SUFFIX
CJ_SUFFIX = settings.CJ_SUFFIX
JX_SUFFIX = settings.JX_SUFFIX


class NoticePipeline(object):

    def process_item(self, item, spider):

        self.types = spider.name
        self.log = Logger(settings.LOG_FILE)
        self.__cj_db = CollectSql('cj', self.log)
        self.__jx_db = CollectSql('jx', self.log)
        self.__config_db = ConfigSql('config', self.log)
        self.list_table = self.types + LIST_SUFFIX if item.get('task_id') is None else FIX_LIST_TABLE
        list_id = item.get('list_id')

        # 采集类型
        if isinstance(item, noticeitems.NoticeNewsItem):    # jbxx
            pass
        #     res = self.jbxx_cj(item)
        # elif isinstance(item, noticeitems.NoticeNewsItem):    # ry
        #     res =  self.ry_cj(item)
        # elif isinstance(item, noticeitems.NoticeNewsItem):    # yj
        #     res =  self.yj_cj(item)
        # elif isinstance(item, noticeitems.NoticeNewsItem):    # xy
        #     res =  self.xy_cj(item)
        else:
            res = None
            # raise DropItem("[Error] 没有定义该item")

        # 公司状态修改
        # if isinstance(item, noticeitems.FlagItem):
        #     self.log.info("this company does't have {types} information...\n".format(types=self.types))
        #     self.__config_db.change_flag(item['table'], item['list_id'])
        # elif res is not None:
        #     self.__config_db.change_flag(self.list_table,list_id)
        # else:
        #    pass

        return res