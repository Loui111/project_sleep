import scrapy
from crawler.items import RegisteredProductsItem
from urllib import parse
import pandas as pd
import configparser

class RegisteredProductsSpider(scrapy.Spider):
    name = 'RegisteredProducts'

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    domain = config['DEFAULT']['DOMAIN']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.RegisteredProductsMiddleware': 100
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.RegisteredProductsPipeline': 300,
        }
    }


    def __init__(self, *args, **kargs):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        domain = config['DEFAULT']['DOMAIN']
        path = config['DEFAULT']['ROOT_PATH']

        xlsx_data = pd.read_excel(path+'/scraping_data2.xlsx', sheet_name='2.searching')

        keyword_list = []

        for word in xlsx_data.values:
            if pd.notna(word[1]):
                temp = word[1]
                keyword_list.append(temp)

        keyword_list.pop(0)
        keyword_list.pop(0)
        keyword_list.pop(0)
        # print(keyword_list)
        self.start_urls = []

        for keyword in keyword_list:
            self.start_urls.append(
                domain+f'/all?query={ keyword }'
            )
            RegisteredProductsItem.keyword = keyword

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')

    def parse(self, response):
        total = response.xpath('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/div[1]/ul/li[1]/a/span[1]/text()').extract_first()

        if total is None:
            total = response.xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/div[1]/ul/li[1]/a/span[1]/text()').extract_first()

        url = response.url
        word = parse.unquote(url.split('=')[1])

        item = {
            'search': word,
            'total': total.strip() if total else total
        }

        print(word, total)

        yield item
