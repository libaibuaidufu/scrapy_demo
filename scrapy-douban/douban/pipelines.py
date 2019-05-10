# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import MySQLdb
class DoubanPipeline(object):
    def process_item(self, item, spider):

        # DBKWARGS=spider.settings.get('DBKWARGS')
        # con=MySQLdb.connect(**DBKWARGS)


        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']
        # 使用的方法2.
        con = MySQLdb.connect(host=host, user=user, passwd=psd, db=db, charset=c)
        # 可以使用的方法1
        # con = MySQLdb.connect(host='127.0.0.1',user='root',passwd='******',db='xiciip',charset='utf8')
        cur = con.cursor()
        sql = ("INSERT INTO douban (name,guanying,pingfen,ftime,text,zan) VALUES(%s,%s,%s,%s,%s,%s)")

        list = [item['name'], item['guanying'],item['pingfen'],item['ftime'],item['text'],item['zan']]


        try:
            cur.execute(sql, list)
            print 'olkkkkkkkkkkkkkKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk'
        except Exception, e:
            print('Insert error', e)
            print 'wocaooooooooooooooooooooooooooooooooooooOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
            con.rollback()

        else:
            con.commit()

        cur.close()
        con.close()

        return item

