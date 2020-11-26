import scrapy
import urllib
import configparser

from crawler.items import CompetitorSalesItem

class CompetitorsalesSpider(scrapy.Spider):
    name = 'CompetitorSales'

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    domain = config['DEFAULT']['DOMAIN']

    allowed_domains = [domain]
    custom_settings = {}

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.CompetitorSalesMiddleware': 100
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.CompetitorSalesPipeline': 300,
        }
    }

    def __init__(self, *args, **kargs):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        domain = config['DEFAULT']['DOMAIN']

        pages = [1, 2 ]

        arg = kargs.get('competitor')
        competitor_list = { 'ProjectSleep': ['프로젝트슬립', 668967, '//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]'],  #PS
                            'Slou': ['슬로우', 657962, '//*[@id="__next"]/div/div[2]/div/div[4]/div[1]/ul/div/div/li/div/div[2]'],  #Slou
                            '3boon1': ['삼분의일', 517390, '//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]'],  # Slou
                            'Lanube': ['라누베', 635613, '//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]'],
                            'Zinus': ['지누스', 656034, '//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div/li/div/div[2]'], #<---
                            'Brandless': ['브랜드리스', 630833, '//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]'],
                            'Sleep-gonggam': ['수면공감', 198235, '//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]'],
                            }

        competitor_info = competitor_list.get(arg)

        competitor = competitor_info[0]
        competitor_code = competitor_info[1]
        competitor_xpath = competitor_info[2]

        self.competitor = competitor
        self.competitor_xpath = competitor_xpath
        competitor = urllib.parse.quote(competitor)

        self.start_urls = []

        for page in pages:
            self.start_urls.append(
                domain+f'/all?frm=NVSHATC&mall={competitor_code}&origQuery={competitor}&pagingIndex={page}&pagingSize=150&productSet=total&query={competitor}&sort=rel&timestamp=&viewType=list'
                # Paging 처리를 해도 max가 걸려 있음. 100이 최대치 인거 같음.
            )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')

    def parse(self, response):
        path = self.competitor_xpath
        contents = response.xpath(path)

        item = CompetitorSalesItem()

        for content in contents:
            product_name = content.xpath('div[1]/a/text()').extract_first()
            price = content.xpath('div[2]/strong/span/span/text()').extract_first()
            buying_cnt = content.xpath('div[5]/a[2]/em/text()').extract_first()

            intPrice = price
            intBuying_cnt = buying_cnt

            print(product_name, intPrice, intBuying_cnt)

            item['PRODUCT_name'] = product_name.strip() if product_name else product_name
            item['Price'] = intPrice.strip() if intPrice else intPrice
            item['buying_cnt'] = intBuying_cnt.strip() if intBuying_cnt else intBuying_cnt

            yield item
