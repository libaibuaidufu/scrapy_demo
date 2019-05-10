# coding:utf-8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re
import csv
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding("utf-8")

class DouBanMovie(object):
    def datastore(self,data):
        #这里面的mysql数据库和表都是事先创建好的
        con = MySQLdb.connect(host='127.0.0.1',user='root',
                              passwd='950916',db='zhihu',charset='utf8')
        cur = con.cursor()
        sql = ("INSERT INTO doubanmovie (name,num) VALUES(%s,%s)")
        list =[data['name'],data['num']]

        try:
            cur.execute(sql,list)
        except Exception,e:
            print e
            con.rollback()
        else:
            con.commit()

        cur.close()
        con.close()

    def get_doubanmovie(self,driver):
        data={}
        page_num = 0
        page = 0
        hah =True
        ele_jiazai = driver.find_element_by_class_name('more')
        for i in range(5):
            js = "window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(js)
            time.sleep(3)
            ele_jiazai.click()
            time.sleep(3)
        while hah:
            hml_const = driver.page_source
            soup =BeautifulSoup(hml_const,'html.parser')
            neirongs = soup.find_all(class_='item')
            for neirong in neirongs:
                num = neirong.div['data-id']
                name = neirong.p.text.replace("  ", "").replace(" ", "").replace("\n","").strip()
                data['num'] = num
                data['name']=name
                print name
                print num
                self.datastore(data)
                data={}
            break


    def crwal(self, root_url):
        driver = webdriver.Chrome(executable_path='C:\Python27\chromedriver.exe')
        # 初始化火狐
        driver.set_page_load_timeout(50)
        # 加载页面 超时50s
        driver.get(root_url)
        # 加载页面
        # driver.maximize_window()  # 将浏览器最大化显示
        driver.implicitly_wait(10)  # 控制间隔时间，等待浏览器反应
        self.get_doubanmovie(driver)
if __name__ =='__main__':
    douban =DouBanMovie()
    douban.crwal('https://movie.douban.com/explore#!type=movie&tag=热门&sort=recommend&page_limit=20&page_start=40')


