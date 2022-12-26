# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem
from scrapy.utils import log

import pymongo

class NewsCrawlerPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self,
        mongo_server,
        mongo_port,
        mongo_db,
    ):
        connection = pymongo.MongoClient(
            mongo_server,
            mongo_port,
        )
        self.db = connection[mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            mongo_server = settings.get('MONGO_SERVER'),
            mongo_port = settings.get('MONGO_PORT'),
            mongo_db = settings.get('MONGO_DB'),
        )

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.insert_one(dict(item))
        # log.msg("News added to MongoDB",
        #         level=log.DEBUG, spider=spider)
        
        return item