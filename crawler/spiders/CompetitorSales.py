import scrapy
import urllib
import configparser

from crawler.items import CompetitorSalesItem
from crawler.util.StrToInt import StrToInt
from crawler.util.getCompetitorList import getCompetitorList

class CompetitorsalesSpider(scrapy.Spider):
    name = 'CompetitorSales'    #스파이더 이름.

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    domain = config['DEFAULT']['DOMAIN']
    config.sections()

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

        pages = [1, 2 ]     #paging을 최대 2페이지. 조절가능.

        arg = kargs.get('competitor')
        #run configuration의 competitor 항목을 읽어옴. crawl CompetitorSales -a competitor=ProjectSleep

        #위의 configuration에서 읽어온 competitor ('ProjectSleep') 으로 아래 정보를 읽어옴.
        #ProjectSleep=프로젝트슬립,668967,//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]
        competitor_info = getCompetitorList(self).get(arg)

        competitor = competitor_info[0]         #프로젝트슬립
        competitor_code = competitor_info[1]    #668967
        competitor_xpath = competitor_info[2]   #//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div/li/div/div[2]

        self.competitor = competitor
        self.competitor_xpath = competitor_xpath
        competitor = urllib.parse.quote(competitor)

        self.start_urls = []

        for page in pages:          #받아온 competitor와 competitor_code 를 넣어서 list에 넣음 (호출은 나중에)
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

            if price is not None:       #가격정보가 없는경우 오류가남.
                intPrice = StrToInt(self, price)    #가격정보가 있으면, 숫자만 남김 ('139,000원' --> 139000 )
            else:
                intPrice = 0            #가격정보가 없을경우는 0을 넣음.

            if buying_cnt is not None:  #구매량 없는경우 오류가남.
                intBuying_cnt = StrToInt(self, buying_cnt)  #구매량이 있으면, 숫자만 남김 ('12,345' --> 12345 )
            else:
                intBuying_cnt = 0       #구매량이 없을땐 0.

            item['PRODUCT_name'] = product_name.strip() if product_name else product_name
            item['Price'] = intPrice
            item['buying_cnt'] = intBuying_cnt

            print(product_name, intPrice, intBuying_cnt)

            yield item
