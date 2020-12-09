import scrapy
import urllib
import configparser

from crawler.items import KeywordallproductsItem
from crawler.util.getKeywordallproducts import getKeywordallproducts
from crawler.util.StrToInt import StrToInt

class KeywordallproductsSpider(scrapy.Spider):
    name = 'KeywordAllproducts'     #스파이더 이름.

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')     #config.ini호출.
    domain = config['DEFAULT']['DOMAIN']            #DOMAIN=https://search.shopping.naver.com/search

    allowed_domains = [domain]
    custom_settings = {     #middleware 설정, pipeline설정.
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

        keyword_list = getKeywordallproducts(self)  #crawler.util.getKeywordallproducts 호출.

        self.start_urls = []
        for keyword in keyword_list:                #받아온 keywordlist 를 하나씩 받아서 처리.
            # keyword = urllib.parse.quote(keyword)       #encoding 처리
            self.keyword = keyword
            for page in pages:
                self.start_urls.append(         #위에서 받은 keyword를 하나씩 넣고 list에 넣음(호출은 아래에서 나중에함)
                    domain+f'/all?frm=NVSHAKW&origQuery={keyword}&pagingIndex={page}&pagingSize=150&productSet=total&query={keyword}&sort=rel&timestamp=&viewType=list'
                    # Paging 처리를 해도 max가 걸려 있음. 100이 최대치 인거 같음.
                )

    def start_requests(self):
        for url in self.start_urls:     #keyword+pagenum를 합친 url을 여기서 하나씩 호출함.
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')
                    #yield. return이랑 동일한 의미이며, 위의 url로 받은 결과를 리턴함.

    def parse(self, response):
        # contents = response.xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]')
        contents = response.xpath('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div/li/div/div[2]')
                #Xpath앞부분 선언.


        item = KeywordallproductsItem() #결과값을 저장할 Item을 호출함.

        for content in contents:    #Xpath로 받아온 결과를 product_name, price, buying_cnt로 세분화 해서 나눔.
            product_name = content.xpath('div[1]/a/text()').extract_first()
            price = content.xpath('div[2]/strong/span/span/text()').extract_first()
            buying_cnt = content.xpath('div[5]/a[2]/em/text()').extract_first()

            print(product_name, price, buying_cnt)  #  화면에 출력함. 이건 없어도됨

            if price is not None:       #가격정보가 없는경우 오류가남.
                intPrice = StrToInt(self, price)    #가격정보가 있으면, 숫자만 남김 ('139,000원' --> 139000 )
            else:
                intPrice = 0            #가격정보가 없을경우는 0을 넣음.

            if buying_cnt is not None:  #구매량 없는경우 오류가남.
                intBuying_cnt = StrToInt(self, buying_cnt)  #구매량이 있으면, 숫자만 남김 ('12,345' --> 12345 )
            else:
                intBuying_cnt = 0       #구매량이 없을땐 0.

            #url에서 query= 항목 받아오기.
            base_url = content.root.base_url
            temp1 = base_url[base_url.find('query'):]
            temp2 = temp1.find('&')
            keyword = urllib.parse.unquote(temp1[6:temp2])

            #xpath로 받아온 값들을 전부 item데이터구조에 전부 적재함.
            item['Keyword'] = keyword
            item['Product_name'] = product_name.strip() if product_name else product_name
            item['price'] = intPrice
            item['buying_cnt'] = intBuying_cnt

            yield item  #전부 적재한 item을 리턴함 (pipeline 한테 갖다줌)
