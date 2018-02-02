#-*- coding:UTF-8 -*-
from __future__ import unicode_literals
from .database import mydb
from news import settings



__metaclass__ = type
RANDOM_TIME = [x for x in range(0,16)]
class ConfigSql(mydb):
    """
    调度库相关
    """
    def __init__(self, types='config', log = None):
        self.type = types
        self.__cj_times_table = settings.TABLES['cj_times_table']
        self.__cj_status_table = settings.TABLES['cj_status_table']
        MYSQL_DB = settings.MYSQL_DATA
        MYSQL_DB['database'] = settings.MYSQL_DB[types]
        super(ConfigSql, self).__init__(MYSQL_DB, log)

    def change_times(self, table):
        """
        修改某表的采集次数
        :param table:str
        :return:
        """
        times = self.get_times(table)

        if times == 1:
            up_sql = "INSERT INTO " + self.__cj_times_table + "(cj_table_name,times) VALUES('" + table + "', 2)"
            self.execute(up_sql)
        else:
            up_sql = "UPDATE " + self.__cj_times_table + " SET times=" + str(times+1)
            self.execute_rowcount(up_sql)

        self.log.info(table+"第 " +str(times-1)+ "入库成功!\n")

    def get_times(self, table):
        """
        获取某表的当前采集次数
        :param table:
        :return:
        """
        sql = "SELECT times FROM " + self.__cj_times_table + " WHERE cj_table_name='{table}'".format(table=table)
        res = self.get(sql)
        if res:
            times = res['times']
        else:
            times = 1
            sql = "INSERT INTO {0}(`cj_table_name`,`times`) VALUES('{1}',2)".format(self.__cj_times_table, table)
            print (sql)
            self.execute_rowcount(sql)
        return times

    def status_restart(self, table):
        """
        重置任务为可采集
        :param table: str
        :return:
        """
        sql = "UPDATE " + self.__cj_status_table + " SET flag=1 WHERE cj_table_name=%s"
        par = [table]
        self.execute_rowcount(sql, par)

    def change_flag(self, table, id, flag='2'):
        """
        修改公司的采集状态
        :param table:
        :param id:
        :param flag:
        :return:
        """
        sql = "UPDATE " + table + " SET flag=%s WHERE id=%s"
        par = [flag, str(id)]
        self.execute_rowcount(sql,par)





if __name__ == '__main__':
    t = ConfigSql()
