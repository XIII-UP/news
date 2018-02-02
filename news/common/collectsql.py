#-*- coding:UTF-8 -*-
from __future__ import unicode_literals
from news.common.database import mydb
from news import settings

__metaclass__ = type
class CollectSql(mydb):
    """
    采集、解析库相关
    """
    def __init__(self, types='cj', log = None):
        self.type = types
        MYSQL_DB = settings.MYSQL_DATA
        MYSQL_DB['database'] = settings.MYSQL_DB[types]
        super(CollectSql, self).__init__(MYSQL_DB, log)

    def c_insert(self, table, content):
        if not table:
            print("数据表为空!!!\n")
            return None

        if not content:
            print("内容为空!!!\n")
            return None

        str_content = ""
        par = []

        try:
            del content['list_id']
        except Exception:
            pass

        if content.get('task_id')is None:
            try:
                del content['task_id']
            except Exception:
                pass

        for cons in content:
            str_content += "`" + cons + "`,"
            par.append(str(content[cons] if content[cons] is not None else ""))

        try:
            str_content = str_content[:-1]
            str_len = len(content)  # 字典元素个数
            str_s = "%s," * str_len  # 格式化字符串个数
            str_s = str_s[:-1]

            sql = "INSERT INTO " + table + "({str_content}) VALUES ({str_s})".format(str_content=str(str_content), str_s=str(str_s))
            # sql = "INSERT INTO " + table + "(" + str(str_content) + ") VALUES (" + str(str_s) + ")"
            res = self.execute(sql, par)

        except Exception as e:
            res = None
            self.log.info(str(e) + "\n")

        return res

    def c_insert_many(self, table, filed, par):
        if not table:
            print("数据表为空!!!\n")
            return None

        if not filed:
            print("内容为空!!!\n")
            return None

        filed_content = ""

        for cons in filed:
            filed_content += "`" + cons + "`,"

        try:
            filed_content = filed_content[:-1]
            filed_len = len(filed)  # 字典元素个数
            filed_s = "%s," * filed_len  # 格式化字符串个数
            filed_s = filed_s[:-1]

            sql = "INSERT INTO " + table + "({filed_content}) VALUES ({filed_s})".format(filed_content=str(filed_content), filed_s=str(filed_s))
            res = self.executemany(sql, par)

        except Exception as e:
            res = None
            self.log.info(str(e) + "\n")

        return res


    def c_update(self, table, content):
        pass

    def c_delet(self, table, content):
        pass