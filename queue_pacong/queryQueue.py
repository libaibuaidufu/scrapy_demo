#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/23 15:27
# @author  : libaibuaidufu
# @File    : taskWorker.py
# @Software: PyCharm


# !/usr/bin/env python
# _*_ coding:utf-8 _*_
""" a work manager sample """
import queue
from multiprocessing.managers import BaseManager
import time
import requests
from bs4 import BeautifulSoup
import queue
import random
from multiprocessing.managers import BaseManager

__author__ = 'Devin -- http://zhangchuzhao.site'


class QueueManager(BaseManager):
    pass


class SacvImage():
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive', 'Host': 'www.27270.com', 'If-Modified-Since': 'Sat, 22 Dec 2018 19',
            'If-None-Match': 'W/"5c1e8fff-b918"', 'Referer': 'https', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

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
        self.num = 0

    def main(self):
        print(self.result.qsize())
        print(self.task.qsize())



if __name__ == '__main__':
    # test()
    sace = SacvImage()
    sace.main()
    print('worker exit!')
