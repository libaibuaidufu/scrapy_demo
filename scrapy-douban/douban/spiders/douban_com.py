# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
import re
import urllib,urllib2
from scrapy.http import Request,FormRequest
from ..items import DoubanItem
import MySQLdb

class DoubanComSpider(CrawlSpider):
    name = 'douban.com'
    allowed_domains = ['douban.com']
    i = 0
    a = 0
    user_url = 'https://movie.douban.com/subject/{movieid}/comments?start={start}&limit={limit}&sort={sort}&status={status}&percent_type={percent_type}'
    con = MySQLdb.connect(host='127.0.0.1',user='root',
                          passwd='950916',db='zhihu',charset='utf8')
    cur = con.cursor()
    cur.execute("SELECT num from doubanmovie")
    data = cur.fetchall()


    def start_requests(self):
        return [Request('https://accounts.douban.com/login?source=movie',
                        meta={'cookiejar': 1},
                callback=self.post_login)]
    def post_login(self, response):
        print 'Preparing login====', response.url
        # s = 'index_nav'
        html = urllib2.urlopen(response.url).read()
        # print 'htnl:', html
        # 验证码图片地址
        imgurl = re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
        if imgurl:
            url = imgurl.group(1)
            # 将图片保存至同目录下
            res = urllib.urlretrieve(url, 'v.jpg')
            # 获取captcha-id参数
            captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
            if captcha:
                vcode = raw_input('请输入图片上的验证码：')
                return [FormRequest.from_response(response,
                                                  method='POST',
                                                  meta={'cookiejar': response.meta['cookiejar']},
                                                  formdata={
                                                      'source': 'movie',
                                                      # 'source': s,
                                                      'form_email': 'xxxxxxxxxx',#自己帐号
                                                      'form_password': 'xxxxxxxxx',#自己的密码 下面一样
                                                      'captcha-solution': vcode,
                                                      'captcha-id': captcha.group(1),
                                                      'login': '登录',
                                                      'remember':'on',
                                                      'redir':'https://movie.douban.com/subject/27038183/comments?status=P'
                                                  },
                                                  callback=self.parse,
                                                  dont_filter=True)
                        ]
        return [FormRequest.from_response(response,
                                          method='POST',
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          formdata={
                                              'source': 'index_nav',
                                              # 'source': s,
                                              'form_email': 'xxxxxxxxxxxxx',
                                              'form_password': 'xxxxxxxxxx'
                                          },
                                          callback=self.after_login,
                                          dont_filter=True)
                ]
    def after_login(self,response):
        print response.xpath("//*[@class='bn-more']/span/text()").extract()[0]
        if response.xpath("//*[@class='bn-more']/span/text()").extract()[0] =="更多":
            print 'cuole'
        else:
            print 'ok'

        i = self.i
        a = self.a
        return [Request(
           self.user_url.format(movieid=self.data[a],start=i, limit=20, sort='new_score', status='P', percent_type=""),
            meta ={'cookiejar':response.meta['cookiejar']},
            callback=self.parse,
            errback=self.parse_err)
        ]
    def jiaa(self):
        self.a +=1
        return self.a


    def parse(self,response):
        neirongs = response.xpath("//*[@class='comment']")
        for neirong in neirongs:
            print response.xpath("//*[@class='bn-more']/span/text()").extract()[0]
            name = neirong.xpath(".//*[@class='comment-info']/a/text()").extract()[0]
            guanying = neirong.xpath(".//*[@class='comment-info']/span[1]/text()").extract()[0]
            pingfen = neirong.xpath(".//*[@class='comment-info']/span/@title").extract()[0]
            try:
                ftime =neirong.xpath(".//*[@class='comment-info']/span[3]/text()").extract()[0].strip()
            except Exception,e:
                print  e
                ftime=1970-1-1
                pass
            text =neirong.xpath(".//p/text()").extract()[0].strip()
            zan = neirong.xpath(".//*[@class='votes']/text()").extract()[0]
            item = DoubanItem(name=name, guanying=guanying, pingfen=pingfen, ftime=ftime,text=text,zan=zan)
            yield item
        next_page= response.xpath("//*[@class='next']/@href").extract()[0]
        href = response.urljoin(next_page)
        print href
        if href:
            yield Request(href,meta ={'cookiejar':response.meta['cookiejar']},
                callback=self.parse,
                errback=self.parse_err)
        else:
            # return [Request(
            #     self.user_url.format(movieid=self.data[a], start=i, limit=20, sort='new_score', status='P',percent_type=""),
            #     meta={'cookiejar': response.meta['cookiejar']},
            #     callback=self.parse,
            #     errback=self.parse_err)]
            #python3.3以上就可以使用这个注释里面的 就不用在定义函数next_movie
            self.next_movie(response)
    def next_movie(self,response):
        a = self.jiaa()
        i = self.i
        return [Request(
            self.user_url.format(movieid=self.data[a], start=i, limit=20, sort='new_score', status='P',
                                 percent_type=""),
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.parse,
            errback=self.parse_err)]

    def parse_err(self, response):
        self.logger.error('crawl %s fail' % response.url)

