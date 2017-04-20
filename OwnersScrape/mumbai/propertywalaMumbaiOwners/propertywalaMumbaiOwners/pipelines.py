import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os


class PropertywalamumbaiownersPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = 'unknown.jpg'
        data_id = 'full/'
        if 'photos/' in request.url:
            data_id = request.url.split('photos/')[1].split('/')[1].split('.')[0]
            image_guid = os.path.join(data_id, request.url.split('photos/')[1].split('/')[1])
        elif 'uservcard' in request.url:
            image_guid = os.path.join(data_id, request.url.split('uservcard/')[1].split('/')[1])
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
