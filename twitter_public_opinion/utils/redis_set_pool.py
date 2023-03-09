# -*- coding: utf-8 -*-
"""
Created on 2023/03/03 10:14

@author: hao.hu
"""
import redis
import time


class IndexTool(object):
    def __init__(self, host, port, pwd, db):
        self.ttl = 7 * 24 * 60 * 60
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=pwd,
            db=db,
            decode_responses=True
        )
        self.debug = False

    def _get_conn(self):
        conn = redis.Redis(connection_pool=self.pool, decode_responses=True)
        return conn

    def get(self, key, field):
        if self.debug:
            key = key + '@debug'
        conn = self._get_conn()
        val = conn.hget(key, field)
        return val

    def get_all(self, key):
        if self.debug:
            key = key + '@debug'
        conn = self._get_conn()
        val = conn.hgetall(key)
        return val

    def set(self, key, field, val):
        if self.debug:
            key = key + '@debug'
        conn = self._get_conn()
        ret = conn.hset(key, field, str(val))
        conn.hset(key, 'last_modify', str(time.time()))
        conn.expire(key, self.ttl)
        return ret

    def hdel(self, key, field):
        if self.debug:
            key = key + '@debug'
        conn = self._get_conn()
        ret = conn.hdel(key, field)
        return ret

    def set_str(self, key, val):
        if self.debug:
            key = key + '@debug'
        conn = self._get_conn()
        ret = conn.set(key, val)
        conn.expire(key, self.ttl)
        return ret
