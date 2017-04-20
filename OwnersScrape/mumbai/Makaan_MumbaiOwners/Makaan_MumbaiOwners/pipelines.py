# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os


class MakaanPunesalePipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_fold = request.url.split('.com/')[1].split('/')[1].split('/')[0]
        image_name = request.url.split('/')[len(request.url.split('/'))-1].split('?')[0]
        image_guid = os.path.join(image_fold, image_name)
        return image_guid

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_path'] = image_paths
        return item
