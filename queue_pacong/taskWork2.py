#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/23 16:08
# @author  : libaibuaidufu
# @File    : taskWork2.py
# @Software: PyCharm
import queue
from multiprocessing.managers import BaseManager
import time
import requests
import datetime

__author__ = 'Devin -- http://zhangchuzhao.site'


class QueueManager(BaseManager):
    pass

class getSave():
    def __init__(self):
        # 从网络上获取Queue
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')

        # 连接服务器
        server_addr = '127.0.0.1'
        print('Connect to server %s ...' % server_addr)
        self.manager = QueueManager(address=(server_addr, 5000), authkey='abc'.encode("utf8"))
        self.manager.connect()

        # 获取Queue对象
        self.task = self.manager.get_task_queue()
        self.result = self.manager.get_result_queue()
        self.now = int(time.time())

    def saveTis(self):
        # 从task队列取任务，并把结果写入result队列
        first = True
        num = 228
        wait = 1
        while first:
            try:
                n = self.result.get(timeout=10)
                print('run task %s ...' % (n))
                if not n:
                    continue
                img_type = n.split(".")[-1]
                r = requests.get(n)
                with open(f"{self.now}-{num}.{img_type}", "wb") as fa:
                    fa.write(r.content)
                num += 1
            except Exception as e:
                time.sleep(5)
                wait += 1
                print(e)
                if wait==12:
                    first=False
                    # break
    def close(self):
        print('worker exit!')

if __name__ == '__main__':
    sa = getSave()
    sa.saveTis()