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

    def saveii(self,url):
        res = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(res.content)
        try:
            try:
                image_url = soup.select("div #picBody p a img")[0]["src"]
            except:
                image_url = soup.select("#viewPic")[0]["href"]
            return image_url
        except Exception as e:
            print(e)
            return None


    def getImage(self,url):
        res = requests.get(url, headers=self.headers)
        # with open("url.html", "r") as f:
        #     html = f.read()
        soup = BeautifulSoup(res.content)
        imageList = []
        try:
            try:
                image_url = soup.select("div #picBody p a img")[0]["src"]
            except Exception as e:
                image_url = soup.select("#viewPic")[0]["href"]
                print(url,image_url)
            imageList.append(image_url)
            li_num = soup.select("#pageinfo")[0]["pageinfo"]
            self.num += int(li_num)
            print(int(li_num))
            for z in range(2, int(li_num)):
                n = url.replace(".html", "")
                imageurl = self.saveii(f"{n}_{z}.html")
                imageList.append(imageurl)
            print(self.num)
            return imageList
        except Exception as e:
            print("aa")
            print(e)
            return imageList

    def main(self):
        print(self.result.qsize())
        print(self.task.qsize())

        # 从task队列取任务，并把结果写入result队列
        first = True
        num = 0
        while first:
            try:
                n = self.task.get(timeout=1)
                print('run task %s ...' % (n))
                urls = self.getImage(n)
                # r = '%d * %d = %d' % (n, n, n * n)
                time.sleep(1)
                if not urls:
                    continue
                for url in urls:
                    if url:
                        self.result.put(url)
            except queue.Empty:
                time.sleep(5)
                num += 1
                print('task quue is empty')
                if num == 15:
                    first = False
def test():
    url = "https://www.27270.com/ent/meinvtupian/2018/313564.html"
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive', 'Host': 'www.27270.com', 'If-Modified-Since': 'Sat, 22 Dec 2018 19',
            'If-None-Match': 'W/"5c1e8fff-b918"', 'Referer': 'https', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    res = requests.get(url, headers=headers)
    # with open("url.html", "r") as f:
    #     html = f.read()
    soup = BeautifulSoup(res.content)
    imageList = []
    # try:
        # try:
    image_url = soup.select("div #picBody p a img")[0]["src"]
    # except Exception as e:
    #     print(e)
    #     image_url = soup.select("#viewPic")[0]["href"]
    #     if "java" in image_url:
    #         raise
    # except Exception as e:
    #     print(e)
    #     image_url = soup.select("#viewPic")[0]["href"]
    print(image_url)
    imageList.append(image_url)
    li_num = soup.select("#pageinfo")[0]["pageinfo"]
    print(int(li_num))
    for z in range(2, int(li_num)):
        n = url.replace(".html", "")
        print(f"{n}_{z}.html")
        # imageurl = saveii(f"{n}_{z}.html")
        imageList.append(n)
    # print(self.num)
    return imageList
    # except RecursionError as e:
    #     print("aa")
    #     print(e)
    #     return imageList

def saveii(url):
    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive', 'Host': 'www.27270.com', 'If-Modified-Since': 'Sat, 22 Dec 2018 19',
            'If-None-Match': 'W/"5c1e8fff-b918"', 'Referer': 'https', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content)
    try:
        try:
            image_url = soup.select("div #picBody p a img")[0]["src"]
        except:
            image_url = soup.select("#viewPic")[0]["href"]
        return image_url
    except Exception as e:
        print(e)
        return None
if __name__ == '__main__':
    # test()
    sace= SacvImage()
    sace.main()
    print('worker exit!')
