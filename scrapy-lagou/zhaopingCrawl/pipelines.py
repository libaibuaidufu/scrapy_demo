# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
class ZhaopingcrawlPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_NAME']
        client = pymongo.MongoClient()
        tdb = client[dbname]
        self.post = tdb[settings['MONGODB_TABLE']]

    # def __init__(self,mongo_uri,mongo_db):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db
    #
    # @classmethod
    # def form_crawler(cls,crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db = crawler.settings.get('MONGO_DATABASE','lagouwang')
    #     )
    # def open_spider(self,spider):
    #     self.client = pymongo.MongoClient(self.mongo_uri)
    #     self.db = self.client[self.mongo_db]
    #
    # def close_spider(self,spider):
    #     self.client.close()

    def process_item(self, item, spider):
        self.post.insert(dict(item))
        return item
