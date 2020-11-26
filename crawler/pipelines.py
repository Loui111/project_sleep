# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exporters import CsvItemExporter
import datetime
import configparser

class CompetitorSalesPipeline(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')

        nowDate = datetime.datetime.now()
        now = nowDate.strftime("%Y%m%d_%H%M%S")

        self.path = config['DEFAULT']['ROOT_PATH']
        self.file = open(self.path+"/results/CompetitorSales/data/CompetitorSales" + now + ".csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class KeywordallproductsPipeline(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')

        nowDate = datetime.datetime.now()
        now = nowDate.strftime("%Y%m%d_%H%M%S")

        self.path = config['DEFAULT']['ROOT_PATH']
        self.file = open(self.path+"/results/Keywordallproducts/Keywordallproducts" + now + ".csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



class PSRankingPipeline(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')

        nowDate = datetime.datetime.now()
        now = nowDate.strftime("%Y%m%d_%H%M%S")

        self.path = config['DEFAULT']['ROOT_PATH']
        self.file = open(self.path+"/results/PSRanking/PSRanking" + now + ".csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class RegisteredProductsPipeline(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')

        nowDate = datetime.datetime.now()
        now = nowDate.strftime("%Y%m%d_%H%M%S")

        self.path = config['DEFAULT']['ROOT_PATH']
        self.file = open(self.path+"/results/RegisteredProducts/RegisteredProducts" + now + ".csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# class NaverRankCsvPipeline(object):
#     def __init__(self):
#         config = configparser.ConfigParser()
#         config.read('config.ini', encoding='utf-8')
#
#         nowDate = datetime.datetime.now()
#         now = nowDate.strftime("%Y%m%d_%H%M%S")
#
#         self.path = config['DEFAULT']['ROOT_PATH']
#         self.file = open(self.path+"/crawler/result/naverRank"+now+".csv", 'wb')
#         self.exporter = CsvItemExporter(self.file, encoding='utf-8')
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
# class NaverShopCsvPipeline(object):
#     def __init__(self):
#
#         config = configparser.ConfigParser()
#         config.read('config.ini', encoding='utf-8')
#
#         nowDate = datetime.datetime.now()
#         now = nowDate.strftime("%Y%m%d_%H%M%S")
#
#         self.path = config['DEFAULT']['ROOT_PATH']
#         self.file = open(self.path+"/crawler/result/naverShop"+now+".csv", 'wb')
#         self.exporter = CsvItemExporter(self.file, encoding='utf-8')
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item