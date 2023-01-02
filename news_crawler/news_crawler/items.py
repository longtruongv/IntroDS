# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlerItem(scrapy.Item):
    _id = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()

class BaoMoiItem(NewsCrawlerItem):
    category = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    abstract = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    keywords = scrapy.Field()

class VnExpressItem(NewsCrawlerItem):
    category = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    abstract = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()



