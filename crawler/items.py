# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CompetitorSalesItem(scrapy.Item):
    PRODUCT_name = scrapy.Field()
    Price = scrapy.Field()
    buying_cnt = scrapy.Field()

class KeywordallproductsItem(scrapy.Item):
    Keyword = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    buying_cnt = scrapy.Field()

class PSRankingItem(scrapy.Item):
    Keyword = scrapy.Field()
    Total = scrapy.Field()
    psRank = scrapy.Field()

class RegisteredProductsItem(scrapy.Item):
    keyword = scrapy.Field()
    total = scrapy.Field()

class ShopItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()

class RankItem(scrapy.Item):
    keyword = scrapy.Field()
    total = scrapy.Field()

