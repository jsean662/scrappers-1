# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import FilesPipeline
from scrapy.exceptions import DropItem
import os


class PublicsectorinfoPipeline(object):
    def process_item(self, item, spider):
        return item


class GovernmentPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        data_id = 'full/'
        # 'http://dpe.gov.in/sites/default/files/brij_singh_141220130001.pdf'
        image_guid = os.path.join(data_id, request.url.split('files/')[1].split('.pdf')[0])
        # image_p = os.path.join(image_guid, request.url.split('/')[len(request.url.split('/')) - 1])
        return image_guid

    def get_media_requests(self, item, info):
        for image_url in item['file_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no images")
        item['file_path'] = file_paths
        return item
