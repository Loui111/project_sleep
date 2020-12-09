import scrapy
import pandas as pd
import urllib
import configparser

from crawler.items import PSRankingItem
from urllib import parse
from crawler.util.UrlDecoding import url_decoding
from crawler.util.getPSRankingKeywords import getPSRankingKeywords
from crawler.util.StrToInt import StrToInt

class PsrankingSpider(scrapy.Spider):
    name = 'PSRanking'

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    domain = config['DEFAULT']['DOMAIN']

    allowed_domains = [domain]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.PSRankingMiddleware': 100
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.PSRankingPipeline': 300,
        }
    }

    def __init__(self, *args, **kargs):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        domain_url = config['DEFAULT']['DOMAIN']
        path = config['DEFAULT']['ROOT_PATH']
        self.company = config['DEFAULT']['COMPANY']

        keywords_list = getPSRankingKeywords(self)
        self.start_urls = []

        pages = [ 1 ]

        # keyword_list1 = ['토퍼매트리스',
        #                  '접이식매트리스',
        #                  '싱글매트리스',
        #                  '바닥매트리스',
        #                  '매트리스싱글',]

        for keyword in keywords_list:
            keyword = urllib.parse.quote(keyword)       #encoding 처리
            for page in pages:
                self.start_urls.append(
                    domain_url+f'/all?frm=NVSHAKW&origQuery={ keyword }&pagingIndex={ page }&pagingSize=150&productSet=total&query={ keyword }&sort=rel&timestamp=&viewType=list'
                # Paging 처리를 해도 max가 걸려 있음. 100이 최대치 인거 같음.
                )

            PSRankingItem.keyword = keyword

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')

    def parse(self, response):
        contents = response.xpath('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div/li/div/div[2]')

        cnt = 0
        ps_list =[]
        item = PSRankingItem()

        for content in contents:

            product_name = content.xpath('div[1]/a/text()').extract_first()
            commercial = content.xpath('div[2]/button/text()').extract_first()    #광고인지 체크

            if not commercial:   #광고가 아니면 None
                if product_name.find(self.company) != -1:
                    print(product_name, str(cnt))
                    ps_list.append(product_name+":: "+str(cnt)+"th")
                cnt=cnt+1
            else:       # 광고인경우
                continue    #광고는 cnt++ 안함.

        total = response.xpath(
            '//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/div[1]/ul/li[1]/a/span[1]/text()').extract_first()
        if total is None:
            total = response.xpath(     #연관검색어가 없는경우 위치가 다름.
                '//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/div[1]/ul/li[1]/a/span[1]/text()').extract_first()

        decoded = url_decoding(self, response.url)

        intTotal = StrToInt(self, total)

        item['Keyword'] = decoded
        item['Total'] = intTotal
        item['psRank'] = ps_list

        yield item
