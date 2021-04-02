# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from pymongo.errors import BulkWriteError

def eval_params(params):
    cust_list = [
        str(x).replace('[','').replace(']','').replace("'", "").replace(',', '') 
        for x in [
                i.split() for i in params
                ] if x!=[]
        ]
    params = dict(zip(cust_list[::2], cust_list[1::2]))
    return params
def eval_price(price):
    return float(
        str(price).replace('[','').replace(']', '').replace("'", "")\
            .replace(',','').replace("\\", "").replace('n', '').split()[0])
        
class LeruaparserPipeline:
    def process_item(self, item, spider):
        item['params'] = eval_params(item['params'])
        item['price'] = eval_price(item['price'])
        item['name'] = item['name'][0]
        return item


class LeruaParserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)
        return item

    def item_completed(self, results, item, info):
    
        for result in [x for ok, x in results if ok]:
            path = result['path']
            
    
            settings = get_project_settings()
            storage = settings.get('IMAGES_STORE')
    
            target_path = os.path.join(storage, item['name'], os.path.basename(path))
            print(target_path)
            path = os.path.join(storage, path)
    
            # If path doesn't exist, it will be created
            if not os.path.exists(os.path.join(storage, item['name'])):
                os.makedirs(os.path.join(storage, item['name']))
    
            if not os.rename(path, target_path):
                raise DropItem("Could not move image to target folder")
    
        if self.IMAGES_RESULT_FIELD in item.fields:
            item[self.IMAGES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item


class MongoPipeline(object):
    def __init__(self):
        MONGO_URI = 'localhost:27017'
        MONGO_DATABASE = 'leroymerlin_db'

        client = MongoClient(MONGO_URI)
        self.mongo_base = client[MONGO_DATABASE]

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.replace_one({"link": item['link']}, item, True)
        return item