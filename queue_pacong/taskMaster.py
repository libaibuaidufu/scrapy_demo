#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/23 15:21
# @author  : libaibuaidufu
# @File    : taskMaster.py
# @Software: PyCharm
import queue
import random
from multiprocessing.managers import BaseManager
from todos.test import get_href
import requests
from bs4 import BeautifulSoup
import time

# 发送任务的队列
task_queue = queue.Queue()
# 接收结果的队列
result_queue = queue.Queue()


class QueueManager(BaseManager):
    pass


class SaceMnage():
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive', 'Host': 'www.27270.com', 'If-Modified-Since': 'Sat, 22 Dec 2018 19',
            'If-None-Match': 'W/"5c1e8fff-b918"', 'Referer': 'https', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        # 把两个queue注册到网络上
        QueueManager.register('get_task_queue', callable=self.get_task_queue)
        QueueManager.register('get_result_queue', callable=self.get_result_queue)
        # 绑定端口5000，设置验证码abc
        self.manager = QueueManager(address=('127.0.0.1', 5000), authkey='abc'.encode('UTF-8'))
        self.manager.start()
        # 通过网络访问Queue对象
        self.task = self.manager.get_task_queue()
        self.result = self.manager.get_result_queue()
        self.num = 1
        # self.url = "https://www.27270.com/word/dongwushijie/"
        # self.url = "https://www.27270.com/ent/meinvtupian/"
        self.url = "https://www.27270.com/ent/meinvtupian/list_11_31.html"


    # 为解决__main__.<lambda> not found问题
    def get_task_queue(self):
        return task_queue

    # 为解决__main__.<lambda> not found问题
    def get_result_queue(self):
        return result_queue

    def main(self):
        self.distributed_task(self.url)
        self.close()

    def distributed_task(self, url):
        self.num += 1
        res = requests.get(url, headers=self.headers)
        # with open("test.html", "r") as f:
        #     html = f.read()
        res.encoding = 'gb18030'
        soup = BeautifulSoup(res.text, 'lxml')
        # soup = BeautifulSoup(res.text)
        resultList = soup.select("div.MeinvTuPianBox ul li")
        # print(resultList)
        print(len(resultList))
        for result in resultList:
            a_list = result.select("a")
            a = a_list[0]
            # a_lists.append(a["href"])
            # return a_lists
            # 添加待处理任务
            # for i in a_lists:
            print('Put task %s ...' % a["href"])
            self.task.put(a["href"])

        for li in soup.select(".NewPages ul li a"):
            if li.text == "下一页":
                nexturl = self.url + li.get("href")
                print(nexturl)
                time.sleep(10)
                while True:
                    if self.task.qsize() <= 60:
                        self.distributed_task(nexturl)

        try:
            nexturl = url[:-1] + str(int(url[-1]) + 1)
            print(nexturl)
            time.sleep(10)
            while True:
                if self.task.qsize() <= 60:
                    self.distributed_task(nexturl)
            # self.distributed_task(nexturl)
        except:
            self.wait()
            # print("not any")
            # if queue.Empty:
            #     return
    def wait(self):
        import time
        time.sleep(6000*3)
        self.manager.shutdown()
    def close(self):
        # 关闭
        self.manager.shutdown()
    def ss(self):
        zurl = "https://www.27270.com/ent/meinvtupian/list_11_212.html"
        url = 'https://www.27270.com/ent/meinvtupian/list_11_'
        # for z in range(1,212+1):
        #     zurl = f'{url}{z}.html'
        #     self.task.put(zurl)
        self.task.put(zurl)
        time.sleep(3600*3)
        self.close()

if __name__ == '__main__':
    sace = SaceMnage()
    sace.main()
    # a_lists = get_href()
    # distributed_task(a_lists)

# soup.div['class']="MeinvTuPianBox"
# print (soup.div.ul)
# with open("test.html","wb") as f:
#     f.write(res.content)
