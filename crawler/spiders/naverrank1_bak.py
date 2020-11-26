import scrapy
from datetime import datetime as dt
from crawler.items import ShopItem
from crawler.items import RankItem

class Naverrank1Spider(scrapy.Spider):
    name = 'naverrank1'
    allowed_domains = ['search.shopping.naver.com']

    def __init__(self, *args, **kargs):
        # today = dt.now().strftime('%Y%m%d')
        queries = ['토퍼매트리스',
                   '접이식매트리스',
                   '싱글매트리스',
                   '바닥매트리스',
                   '매트리스싱글',
                   '토퍼']

        # queries = ['토퍼매트리스',
        #             '접이식매트리스',
        #             '싱글매트리스',
        #             '바닥매트리스',
        #             '매트리스싱글',
        #             '토퍼',
        #             '매트리스토퍼',
        #             '메모리폼토퍼',
        #             '토퍼추천',
        #             '접이식토퍼',
        #             '퀸매트리스',
        #             '매트리스퀸사이즈',
        #             '퀸사이즈매트리스',
        #             '매트리스퀸',
        #             '퀸침대매트리스',
        #             '3단접이식매트리스',
        #             '3단매트리스',
        #             '바닥토퍼',
        #             '차박용품',
        #             '차박매트',
        #             '바닥매트',
        #             '트렁크매트',
        #             '카매트',
        #             '차박매트리스',
        #             '자동차캠핑',
        #             '메모리폼침대매트리스',
        #             '원룸매트리스',
        #             '1인용매트리스',
        #             '매트리스',
        #             '침대매트리스',
        #             '메모리폼매트리스',
        #             '슈퍼싱글매트리스',
        #             '침대메트리스',
        #             '매트리스추천',
        #             '수면안대',
        #             '안대',
        #             '눈안대',
        #             '수면안대추천',
        #             '숙면안대',
        #             '바디필로우',
        #             '롱쿠션',
        #             '긴베개',
        #             '임산부바디필로우',
        #             '임산부베개',
        #             '임산부쿠션',
        #             '소독스프레이',
        #             '살균스프레이',
        #             '스프레이소독제']

        self.start_urls = []

        for query in queries:
            self.start_urls.append(
                f'https://search.shopping.naver.com/search/all?query={ query }'
            )
            # self.keyword = query
            RankItem.keyword = query


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')

    def parse(self, response):
        total = response.xpath('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/div[1]/ul/li[1]/a/span[1]/text()').extract_first()
        RankItem.total = total

        # total['total'] = total.strip() if total else total

        # item = {
        #     'title': title.strip() if title else title
        #     , 'price': price.strip() if price else price
        # }
        print(RankItem.keyword, RankItem.total)

        yield total

    # def parse(self, response):
    #     contents = response.xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div')
    #
    #     for content in contents:
    #         title = content.xpath('/li/div/div[2]/div[1]/a').extract_first()
    #         price = content.xpath('/li/div/div[2]/div[2]/strong/span/span').extract_first()
    #
    #         item = {
    #             'title': title.strip() if title else title
    #             , 'price': price.strip() if price else price
    #         }
    #         print(item)
    #
    #         yield item
