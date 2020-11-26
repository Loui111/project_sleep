import scrapy
from crawler.items import PSRankingItem
from urllib import parse
import pandas as pd
import urllib

from crawler.util.url_decoding import url_decoding

class PsrankingSpider(scrapy.Spider):
    name = 'PSRanking_bak'
    allowed_domains = ['search.shopping.naver.com']
    # start_urls = ['http://search.shopping.naver.com/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.PSRankingMiddleware': 100
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.PSRankingPipeline': 300,
        }
    }

    def __init__(self, *args, **kargs):

        # 근데 이건 나중에 DB를 띄워서 하는게 더 나을거 같은데??
        xlsx_data = pd.read_excel('/Users/genesisjk/project_sleep/scraping_data2.xlsx', sheet_name='1.rank')

        keyword_list = []

        for word in xlsx_data.values:
            if pd.notna(word[3]):
                temp = word[3]
                keyword_list.append(temp)

        keyword_list.remove('키워드')
        # print(keyword_list)
        self.start_urls = []
        #
        # def __init__(self, *args, **kargs):
        #     pages = [1, 2, 3]
        #
        #     self.start_urls = []
        #     for page in pages:
        #         self.start_urls.append(
        #             f'https://search.shopping.naver.com/search/category?catId=50001229&origQuery&pagingIndex={page}&pagingSize=40&productSet=total&query&sort=rel&timestamp=&viewType=list'
        #         )

        # keyword_list1 = ['접이식매트리스'] #테스트
        pages = [ 1 ]

        keyword_list1 = ['토퍼매트리스',
                         '접이식매트리스',
                         '싱글매트리스',
                         '바닥매트리스',
                         '매트리스싱글',]


        for keyword in keyword_list1:
            keyword = urllib.parse.quote(keyword)       #encoding 처리
            for page in pages:
                self.start_urls.append(
                    f'https://search.shopping.naver.com/search/all?frm=NVSHAKW&origQuery={ keyword }&pagingIndex={ page }&pagingSize=150&productSet=total&query={ keyword }&sort=rel&timestamp=&viewType=list'
                # Paging 처리를 해도 max가 걸려 있음. 100이 최대치 인거 같음.
                )

            PSRankingItem.keyword = keyword

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')

    def parse(self, response):
        # contents = response.xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]')
        contents = response.xpath('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div/li/div/div[2]')
        # comecial = response.xpath('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div/li/div/div[2]/div[2]')


        # div[1]/a/text()
        # /button/text()

        cnt = 0
        ps_list =[]
        item = PSRankingItem()

        for content in contents:

            product_name = content.xpath('div[1]/a/text()').extract_first()
            comm = content.xpath('div[2]/button/text()').extract_first()    #광고인지 체크

            if not comm:   #광고가 아니면 None
                if product_name.find('프로젝트') != -1:
                    print(product_name, cnt)
                    ps_list.append(cnt)
                cnt=cnt+1
            else: # 광고인경우
                continue
            # print(cnt)

        total = response.xpath(
            '//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/div[1]/ul/li[1]/a/span[1]/text()').extract_first()
        if total is None:
            total = response.xpath(     #연관검색어가 없는경우 위치가 다름.
                '//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/div[1]/ul/li[1]/a/span[1]/text()').extract_first()

        decoded = url_decoding(self, response.url)

        item['Keyword'] = decoded
        item['Total'] = total.strip() if total else total
        item['psRank'] = ps_list

        yield item


        # for content in contents:
        #     title = content.xpath('div[1]/a/text()').extract_first()
        #     price = content.xpath('div[2]/strong/span/span/text()').extract_first()
        #
        #     print(title, price)
        #
        #     item = PSRankingItem()
        #
        #     item['keyword'] = title.strip() if title else title
        #     item['PSrank'] = price.strip() if price else price
        #
        #     # item = {
        #     #     'title': title.strip() if title else title
        #     #     , 'price': price.strip() if price else price
        #     # }
        #     # print( item )
        #
        #     yield item
