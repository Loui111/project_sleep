from time import sleep
 
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import configparser

class CompetitorSalesMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        path = config['DEFAULT']['ROOT_PATH']

        CHROMEDRIVER_PATH = path+'/crawler/drivers/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        # chrome_options.add_argument( "--headless" )   #브라우저 띄울필요 없을때는 (자동화 완성) 주석 해제
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        self.driver = driver

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)

        for i in range(12):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)

        body = to_bytes(text=self.driver.page_source)

        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

class KeywordallproductsMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        path = config['DEFAULT']['ROOT_PATH']

        CHROMEDRIVER_PATH = path + '/crawler/drivers/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        # chrome_options.add_argument( "--headless" )   #브라우저 띄울필요 없을때는 (자동화 완성) 주석 해제
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        self.driver = driver

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)

        for i in range(12):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)

        body = to_bytes(text=self.driver.page_source)

        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)


class PSRankingMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        path = config['DEFAULT']['ROOT_PATH']

        CHROMEDRIVER_PATH = path + '/crawler/drivers/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        # chrome_options.add_argument( "--headless" )   #브라우저 띄울필요 없을때는 (자동화 완성) 주석 해제
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        self.driver = driver

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)

        for i in range(12):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)

        body = to_bytes(text=self.driver.page_source)

        # sleep( 5 )

        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)


class RegisteredProductsMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        path = config['DEFAULT']['ROOT_PATH']

        CHROMEDRIVER_PATH = path + '/crawler/drivers/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        # chrome_options.add_argument( "--headless" )   #브라우저 띄울필요 없을때는 (자동화 완성) 주석 해제
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        self.driver = driver

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)

        body = to_bytes(text=self.driver.page_source)

        sleep( 1 )

        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)


class SearchingMiddleware(object):
 
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware
 
    def spider_opened(self, spider):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        path = config['DEFAULT']['ROOT_PATH']

        CHROMEDRIVER_PATH = path + '/crawler/drivers/chromedriver'
        WINDOW_SIZE = "1920,1080"
 
        chrome_options = Options()
        # chrome_options.add_argument( "--headless" )   #브라우저 띄울필요 없을때는 (자동화 완성) 주석 해제
        chrome_options.add_argument( "--no-sandbox" )
        chrome_options.add_argument( "--disable-gpu" )
        chrome_options.add_argument( f"--window-size={ WINDOW_SIZE }" )
        
        driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options )
        self.driver = driver
 
    def spider_closed(self, spider):
        self.driver.close()
 
    def process_request( self, request, spider ):
        self.driver.get( request.url )

        for i in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)

        body = to_bytes( text=self.driver.page_source )
 
        # sleep( 5 )
 
        return HtmlResponse( url=request.url, body=body, encoding='utf-8', request=request )

