# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import YunqiBookListItem,YunqiBookDetailItem
from scrapy.http import Request

class YunqiQqComSpider(CrawlSpider):
    name = 'yunqi'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ["http://yunqi.qq.com/bk/so2/n30p1"]

    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):
        print '1111111111111111111111111111111111111111111111111111111111111111111'
        i = 0
        books = response.xpath(".//div[@class='book']")
        for book in books:
            print i
            print len(books)
            novelLink = book.xpath("./div[@class='book_info']/h3/a/@href").extract_first()
            print novelLink
            novelImageUrl = book.xpath("./a/img/@src").extract_first()
            novelId = book.xpath("./div/h3/a/@id").extract_first()
            novelName = book.xpath("./div/h3/a/text()").extract_first()
            novelAuthor = book.xpath("./div/dl[1]/dd[1]/a/text()").extract_first()
            novelStatus = book.xpath("./div/dl[1]/dd[3]/text()").extract_first()
            novelType = book.xpath("./div/dl/dd[2]/a/text()").extract_first()
            novelUpdateTime = book.xpath("./div/dl[2]/dd[1]/text()").extract_first()
            novelWords = book.xpath("./div/dl[2]/dd[2]/text()").extract_first()
            item =YunqiBookListItem(novelAuthor=novelAuthor,novelLink=novelLink,novelId=novelId,novelImageUrl=novelImageUrl,novelStatus=novelStatus,novelName=novelName,novelType=novelType,novelUpdateTime=novelUpdateTime,novelWords=novelWords)
            yield item
            i +=1
            request = Request(url=novelLink, callback=self.parse_book_detail)
            request.meta['novelId'] = novelId

            yield request

    def parse_book_detail(self, response):
        print '22222222222222222222222222222222222222222222222222222222222222'
        novelId = response.meta['novelId']
        novelLabel = response.xpath("//div[@class='tags']/text()").extract_first()

        novelAllClick = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[1]/text()").extract_first()
        novelAllPopular = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[2]/text()").extract_first()
        novelAllComm = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[3]/text()").extract_first()

        novelMonthClick = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[1]/text()").extract_first()
        novelMonthPopular = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[2]/text()").extract_first()
        novelMonthComm = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[3]/text()").extract_first()

        novelWeekClick = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[1]/text()").extract_first()
        novelWeekPopular = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[2]/text()").extract_first()
        novelWeekComm = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[3]/text()").extract_first()
        novelCommentNum = response.xpath(".//*[@id='novelInfo_commentCount']/text()").extract_first()
        bookDetailItem = YunqiBookDetailItem(novelId=novelId, novelLabel=novelLabel, novelAllClick=novelAllClick,
                                             novelAllPopular=novelAllPopular,
                                             novelAllComm=novelAllComm, novelMonthClick=novelMonthClick,
                                             novelMonthPopular=novelMonthPopular,
                                             novelMonthComm=novelMonthComm, novelWeekClick=novelWeekClick,
                                             novelWeekPopular=novelWeekPopular,
                                             novelWeekComm=novelWeekComm, novelCommentNum=novelCommentNum)

        yield bookDetailItem
