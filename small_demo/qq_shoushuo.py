#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 0019 16:40
# @Site    : 
# @File    : qq_shoushuo.py
# @Software: PyCharm

import codecs
import json
import os
import time

from selenium import webdriver
while True:
    other_qq=input("请输入别人qq：")
    own_qq = input("请输入自己qq：")
    own_qq_pw=input("请输入自己qq密码：")
    if input("确认 y ,重新输入 any key ,not y:") == "y":
        break


f = codecs.open(('ls') + u'.html', 'a+',"utf-8")
# f = open("ls.html","a+")
driver=webdriver.Chrome(executable_path="E:\Envs\chromedriver.exe")
driver.get('http://user.qzone.qq.com/{}/311'.format(other_qq))
#这里的qq你可以做成一个 列表  循环 输入进去 爬取一堆 也可以是单个
try:
    driver.find_element_by_id('login_div')
    a = True
except:
    a = False
if a == True:
    driver.switch_to_frame('login_frame')
    driver.find_element_by_id("switcher_plogin").click()
    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('u').send_keys(own_qq)
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('p').send_keys(own_qq_pw)
    driver.find_element_by_id('login_button').click()
    time.sleep(2)
try:
    driver.find_element_by_id('QM_OwnerInfo_Icon')
    b = True
except:
    b = False
if b == True:
    driver.switch_to.frame('app_canvas_frame')
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    content = driver.find_elements_by_css_selector('.content')
    stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
    for con,sti in zip(content,stime):
        data = {
                'qq':other_qq,
                'time':sti.text,
                'shuos':con.text
            }
        print(data)
        f.write(json.dumps(data))
        # f.write(data)
        f.write(os.linesep)
    try:
        driver.find_element_by_link_text('下一页')
        d = True
    except:
        d = False
else:
    d = False
while d:
    try:
        driver.find_element_by_link_text('下一页').click()
        time.sleep(3)
        d = True
    except:
        d = False
    if d == True:
        js = "var q=document.documentElement.scrollTop=100000"
        driver.execute_script(js)
        contents = driver.find_elements_by_css_selector('.content')
        times = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        for c,t in zip(contents,times):
            datas = {
                    'qq':other_qq,
                    'time':t.text,
                    'shuos':c.text
                }
            print(datas)
            f.write(json.dumps(datas))
            f.write(os.linesep)
f.close()