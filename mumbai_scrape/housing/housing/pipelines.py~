# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
class HousingPipeline(object):
    def process_item(self, item, spider):
        return item
'''

from scrapy import signals
from scrapy.exporters import CsvItemExporter

class CSVPipeline(object):

  def __init__(self):
    self.files = {}

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    file = open('%s_items.csv' % spider.name, 'w+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    self.exporter.fields_to_export = ['data_id','Building_name','config_type','Selling_price','Monthly_Rent','lat','longt','platform','city','listing_date','txn_type','property_type','locality','sqft','Status','listing_by','name_lister','Details','address','price_on_req','sublocality','age','google_place_id','immediate_possession','mobile_lister','areacode','management_by_landlord']
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item
