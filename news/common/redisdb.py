# -*- coding:UTF-8 -*-
import redis


# Jon!Q@W#E
class redisdb(object):
    def __init__(self,host='localhost', port=6379, db=1, password = None):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
        self.Redis = redis.Redis(connection_pool=self.pool)

    # push a new link at the end of list
    def pushLink(self, rlist, value):
        return self.Redis.lpush(rlist, value)

    # return the last link
    def lpopLink(self, rlist, value):
        return self.Redis.lpop(rlist)

    # return the first link
    def rpopLink(self, rlist, value):
        return self.Redis.rpop(rlist)

    def brpoplpush(self, src, dst, timeout=10):
        return self.Redis.brpoplpush(src, dst, timeout=10)

    def lrem(self, list_name, key, num=0):
        return self.Redis.lrem(list_name, key, num)

    def lrange(self, list_name, sta, sto):
        return self.Redis.lrange(list_name, sta, sto)

    # get length of list
    def lenList(self, rlist):
        return self.Redis.llen(rlist)

    # init list
    def delList(self, rlist):
        return self.Redis.delete(rlist)

    # get
    def rget(self, key):
        return self.Redis.get(key)

    # delete key
    def delete(self, key):
        return self.Redis.delete(key)

    # all keys
    def rkeys(self):
        return self.Redis.keys()

    # set
    def rset(self, key, value):
        return self.Redis.set(key, value)

    def flushdb(self):
        return self.Redis.flushdb()




