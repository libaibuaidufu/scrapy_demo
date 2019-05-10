# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopingcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    createTime =scrapy.Field()
    positionName =scrapy.Field()
    workYear =scrapy.Field()
    education =scrapy.Field()
    jobNature =scrapy.Field()
    companyShortName =scrapy.Field()
    city =scrapy.Field()
    salary =scrapy.Field()
    district =scrapy.Field()
    companyLabelList =scrapy.Field()
    companySize =scrapy.Field()
    industryLables =scrapy.Field()
    firstType =scrapy.Field()
    secondType =scrapy.Field()
    companyFullName =scrapy.Field()