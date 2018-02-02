#-*- coding:UTF-8 -*-
from __future__ import unicode_literals
from .redisdb import redisdb
from . import configsql
from news import settings

import json
import time

CONFIG_DB = configsql.ConfigSql()
LIMIT = settings.LIMIT
TASK_TABLE = settings.TABLES['task_table']
FIX_GS_LIST = settings.TABLES['fix_company_table']


def set_redis_data( key, table, log, condition=None):
    """
    :param key:
    :param table:
    :param condition:
    :return:
    """
    limit = settings.LIMIT
    task_table = settings.TABLES['task_table']
    company_table = settings.TABLES['fix_company_table']
    where_fix = "flag=0 AND task_id="
    where_all = "flag=0"
    if condition:
        table = company_table

        # 查询任务组中该类型最高优先级的任务对应的id
        sql = "SELECT * FROM " + task_table + " WHERE types=%s AND flag<2 ORDER BY `level` DESC"
        par = [condition]
        res = CONFIG_DB.query(sql, par)

        if res:
            for i in res:
                sql = "SELECT COUNT(id) as c FROM " + table + " WHERE task_id=%s AND flag=0"
                par = [i['id']]
                num = CONFIG_DB.get(sql, par)

                if num['c']:
                    sql = "UPDATE " + task_table + " SET flag=1 WHERE id=%s"

                    if i['flag'] == 0 and not CONFIG_DB.execute_rowcount(sql, par):
                        log.info(key + "ERROR: " + sql + "\n")

                    where = where_fix + str(i['id'])
                    sql = "select * from " + table + " where " + where + " LIMIT " + str(limit)
                    res = CONFIG_DB.query(sql)
                    break
                else:
                    res = None
        else:
            log.info("all task is over\n")
            return None
    else:
        where = where_all
        sql = "select * from " + table + " where " + where + " LIMIT " + str(LIMIT)
        res = CONFIG_DB.query(sql)

    if res:
        for i in res:
            del i['created']
            sql = "update " + table + " set flag=1 where id=" + str(i['id'])
            try:
                CONFIG_DB.execute_rowcount(sql)
            except Exception:
                log.info(key + "ERROR: " + sql + "\n")

        result = json.dumps(res, ensure_ascii=False)

        global REDB

        while True:
            res = REDB.rget(key)
            if res:
                time.sleep(2)
                continue
            else:
                REDB.rset(key, result)
                break
    else:
        log.info(key + "-- result is null\n")


def get_redis_data(key, log,condition=None):
    """
    获取redis中的数据
    :param key:str
    :param condition:str
    :return:dict
    """

    global REDB

    table = key + settings.LIST_SUFFIX
    key += '_list_fix' if condition else '_list_all'
    set_redis_data(key, table, log, condition)

    for i in range(10):

        res = REDB.rget(key)

        CONFIG_DB.log.info("任务" + str(key) + "获取redis数据第 " + str(i) + " 次")
        if res:
            REDB.delete(key)
            break
        time.sleep(5)

    try:
        res = json.loads(res)
    except Exception:
        return None
    else:
        list_dic = {}

        for i in res:
            list_dic[i['qymc']] = {
                'list_id': i['id'],
            }

            try:
                list_dic[i['qymc']]['task_id']= i['task_id']
            except KeyError:
                list_dic[i['qymc']]['task_id'] = None

            if 'jst' in key:
                list_dic[i['qymc']]['jst_id'] = i['gs_id']
            elif 'slsc' in key:
                list_dic[i['qymc']]['gs_id'] = i['gs_id']
            else:
                list_dic[i['qymc']]['gs_id'] = i['gs_id']
                list_dic[i['qymc']]['cname'] = i['cname']

        return list_dic


def set_pid(kind, types, pid):
    """
    当前脚本pid入redis库， 删除了之后才能入下一个
    (不同ip不同库)
    """
    global REDB
    REDB = redisdb(host=settings.REDIS_HOST,
                   port=settings.REDIS_PORT,
                   db=settings.REDIS_DB,
                   password=settings.REDIS_PASSWORD)
    key = types + ('_all' if kind == "all" else "_fix") #全变量判断

    while REDB.rget(key) is not None:
        print ("set_pid to redis..sleep 2s")
        time.sleep(2)

    REDB.rset(key, pid)


def set_redis_data1(key, table, log, condition=None):
    """
    :param key:
    :param table:
    :param condition:
    :return:
    """
    limit = settings.LIMIT
    task_table = settings.TABLES['task_table']
    company_table = settings.TABLES['fix_company_table']
    where_fix = "flag=0 AND task_id="
    where_all = "flag=0 AND task_id is null "
    if condition:
        table = company_table

        # 查询任务组中该类型最高优先级的任务对应的id
        sql = "SELECT * FROM " + task_table + " WHERE types=%s AND flag<2 ORDER BY `level` DESC"
        par = [condition]
        res = CONFIG_DB.query(sql, par)

        if res:

            for i in res:
                sql = "SELECT COUNT(id) as c FROM " + table + " WHERE task_id=%s AND flag=0"
                par = [i['id']]
                num = CONFIG_DB.get(sql, par)

                if num['c']:
                    sql = "UPDATE " + task_table + " SET flag=1 WHERE id=%s"

                    if not CONFIG_DB.execute_rowcount(sql, par):
                       log.info(key + "ERROR: " + sql + "\n")

                    where = where_fix + str(i['id'])
                    break
                else:
                    where = ""
        else:
            log.info("all task is over\n")
            return None
    else:
        where = where_all

    sql = "select * from " + table + " where " + where + " limit " + str(limit)
    res = CONFIG_DB.query(sql)

    if res:
        for i in res:
            del i['created']
            sql = "update " + table + " set flag=1 where id=" + str(i['id'])
            try:
                CONFIG_DB.execute_rowcount(sql)
            except Exception:
                log.info(key + "ERROR: " + sql + "\n")

        result = json.dumps(res, ensure_ascii=False)


        while True:
            res = REDB.rget(key)
            if res:
                time.sleep(2)
                continue
            else:
                REDB.rset(key, result)
                break
    else:
        log.info(key + "-- result is null\n")


def get_del_pid(types, redis_db):
    """
    # 获取已经删除的pid_list列表
    :param key: str
    :param redis_db: int
    :return: list
    """
    global REDB
    REDB = redisdb(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=redis_db, password=settings.REDIS_PASSWORD)

    key = types + "_del"
    count = 0
    while not REDB.lenList(key):
        time.sleep(2)
        count += 1
        if count >10:
            return []

    pis_list = REDB.lrange(key, 0, REDB.lenList(key))
    # REDB.delList(key)

    return pis_list

def clear_del_pid_list(types, redis_db):
    global REDB
    REDB = redisdb(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=redis_db, password=settings.REDIS_PASSWORD)

    key = types + "_del"
    REDB.delList(key)

def add_del_pid(is_all, name, pid):
    key = name + ("_all" if is_all == 1  else "_fix")
    key += '_del'

    print (key + " push pid:" + str(pid))
    REDB.pushLink(key, pid)
