# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
import json, time
from ..items import ZhaopingcrawlItem


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    # start_urls = [
    #     'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false&isSchoolJob=0']
    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    i = 1
    totalPageCount = 0

    def start_requests(self):
        return [FormRequest(
            'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false&isSchoolJob=0',
            formdata={'pn': '{}'.format(self.i),'kd':'python'}, callback=self.parse)]

    def parse(self, response):
        print '--' * 30
        print 'Preparing login====', response.url
        # print response.body
        jdict = json.loads(response.body)
        try:
            jcontent = jdict["content"]
            wawa = jcontent['positionResult']
            jresult = wawa["result"]
            self.totalPageCount = wawa['totalCount'] / 15 + 1
            print self.totalPageCount
            for each in jresult:
                item = ZhaopingcrawlItem(createTime=each['createTime'],
                                         positionName=each['positionName'],
                                         workYear=each['workYear'],
                                         education=each['education'],
                                         jobNature=each['jobNature'],
                                         companyShortName=each['companyShortName'],
                                         city=each['city'],
                                         salary=each['salary'],
                                         district=each['district'],
                                         companyLabelList=each['companyLabelList'],
                                         companySize=each['companySize'],
                                         industryLables=each['industryLables'],
                                         firstType=each['firstType'],
                                         secondType=each['secondType'],
                                         companyFullName=each['companyFullName'])
                yield item
            if self.i <= self.totalPageCount:
                self.i += 1
                print self.i
                print '--'*25
                yield FormRequest(
                    'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false&isSchoolJob=0',
                    formdata={'kd':'python','pn':'{}'.format(self.i)},callback=self.parse)

        except:
            msg = jdict['msg']
            print msg
            print self.i
            print '--' * 25
            yield FormRequest(
                'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false&isSchoolJob=0',
                formdata={'kd':'python','pn':'{}'.format(self.i)}, callback=self.parse)
