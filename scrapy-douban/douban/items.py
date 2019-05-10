# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    guanying=scrapy.Field()
    pingfen=scrapy.Field()
    ftime=scrapy.Field()
    text=scrapy.Field()
    zan=scrapy.Field()


