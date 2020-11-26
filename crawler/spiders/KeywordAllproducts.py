import scrapy
import urllib
import configparser

from crawler.items import KeywordallproductsItem

class KeywordallproductsSpider(scrapy.Spider):
    name = 'KeywordAllproducts'

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    domain = config['DEFAULT']['DOMAIN']

    allowed_domains = [domain]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.KeywordallproductsMiddleware': 100
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.KeywordallproductsPipeline': 300,
        }
    }

    def __init__(self, *args, **kargs):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        domain = config['DEFAULT']['DOMAIN']

        pages = [1 ]

        keyword = '싱글매트리스'
        keyword = urllib.parse.quote(keyword)

        self.start_urls = []
        for page in pages:
            self.start_urls.append(
                domain+f'/all?frm=NVSHAKW&origQuery={keyword}&pagingIndex={page}&pagingSize=150&productSet=total&query={keyword}&sort=rel&timestamp=&viewType=list'
                # Paging 처리를 해도 max가 걸려 있음. 100이 최대치 인거 같음.
            )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')

    def parse(self, response):
        # contents = response.xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]')
        contents = response.xpath('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div/li/div/div[2]')

        item = KeywordallproductsItem()

        for content in contents:
            product_name = content.xpath('div[1]/a/text()').extract_first()
            price = content.xpath('div[2]/strong/span/span/text()').extract_first()
            buying_cnt = content.xpath('div[5]/a[2]/em/text()').extract_first()

            print(product_name, price, buying_cnt)

            item['product_name'] = product_name.strip() if product_name else product_name
            item['price'] = price.strip() if price else price
            item['buying_cnt'] = buying_cnt.strip() if buying_cnt else buying_cnt

            yield item
