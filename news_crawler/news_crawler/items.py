# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BaoMoiItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    abstract = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    keywords = scrapy.Field()

class VnExpressItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    abstract = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()



