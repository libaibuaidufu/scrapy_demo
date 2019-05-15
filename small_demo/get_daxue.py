#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 0014 11:00
# @File    : get_daxue.py
# @author  : dfkai
# @Software: PyCharm
"""
抓取 hao123 上面 大学 名称 和 大学地址
"""
import json
import re
import time

import requests
from bs4 import BeautifulSoup


# 抓取首页链接
def get_index():
    index_url = "http://www.hao123.com/edu"
    headers = get_headers()
    res = requests.get(url=index_url, headers=headers)
    res.encoding = "gb18030"
    soup = BeautifulSoup(res.content, "lxml")
    result_list = soup.select("#bd > div.edu-content.clearfix")
    url_list = []
    for result in result_list:
        data = re.findall("<a href=\"(.*?)\" target=\"_blank\">\[点击查看]</a>", str(result))
        for url in data:
            url_list.append(url)
    return url_list


# 设置headers
def get_headers():
    text = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
    Cache-Control: max-age=0
    Connection: keep-alive
    Cookie: BAIDUID=53BC5A833E12D740A3E7767115A46E89:FG=1; BDUSS=XVLWnkzSlUtSUNFQjRmVlJXb0h-REdKVFdWWS0ycGpZd0FGQW5mT1RQSlpyZ0ZkRVFBQUFBJCQAAAAAAAAAAAEAAAAaZ602X19Dwt5f07Cw119fAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFkh2lxZIdpcZ; hz=0; HAOSTOKEN=bfe77325a20c13fa69839200c25a59a5aaee7e7266aafc98328075cac1319c6d
    Host: www.hao123.com
    If-Modified-Since: Thu, 20 Dec 2018 19:10:12 GMT
    If-None-Match: W/"5c1be914-67ce"
    Referer: http://www.hao123.com/edu
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"""
    headers = {}
    for z in text.split("\n"):
        key = z.split(":")[0]
        value = str(z.split(":")[1])[1:]
        headers[key] = value


# 抓取内容
def get_page_name():
    data_dict = {}
    url_list = get_index()
    for url in url_list:
        data_dict = get_data(url, data_dict)
    return data_dict


# 这里可以写成 多线程试试
def get_data(url, data_dict):
    print(url)
    time.sleep(2)
    try:
        headers = get_headers()
        res = requests.get(url, headers=headers)
        res.encoding = "gb18030"
        data = re.findall("<a href=\"(.*?)\">(.*)?</a></p></td>", str(res.text))
        for href, name in data:
            data_dict[name] = href
            # print(f"{name}: {href}")
        return data_dict
    except:
        return data_dict


# 插入数据库 输入sql语句
def get_insert_sql(data):
    base_sql = "insert into colleges(name,url) VALUES "
    for key, value in data.items():
        base_sql += "('%s','%s')," % (key, value)
    print(base_sql)
    return base_sql


# 写入文件
def write_txt(data):
    with open("data_json.txt", "w+", encoding="utf8") as f:
        f.write(json.dumps(data))

# 读取文件
def read_txt():
    with open("data_json.txt", "r+", encoding="utf8") as f:
        data = f.read()
        data = json.loads(data)
    return data


if __name__ == '__main__':
    data = get_page_name()
