from news_crawler.items import VnExpressItem

import scrapy
from scrapy import Selector
from scrapy.http import Request, Response

from dateutil import parser

CATEGORIES = {
    'thoi-su': 'Thời sự',
    'the-gioi': 'Thế giới',
}

class VnExpressSpider(scrapy.Spider):
    name = 'vnexpress'
    based_url = 'https://vnexpress.net'

    allowed_domains = ['vnexpress.net']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        for category in CATEGORIES.keys():
            url = f'{self.based_url}/{category}'
            yield Request(
                url=url,
                callback=self.parse_news_list,
                meta={'category': category},
            )

    def parse_news_list(self, response: Response, **kwargs):
        category = response.meta.get('category')
        news_list = Selector(response)

        news_url_list = news_list.xpath('//h3[@class="title_news"]/a/@href').extract()
        # news_url_list = ['https://vnexpress.net/le-quyen-ban-trai-thiet-thoi-khi-yeu-toi-4552452.html']
        print("############################################################")
        print(len(news_url_list))
        for news_url in news_url_list:
            news_id = self.extract_id(news_url)
            if not news_id:
                continue

            yield Request(
                url=news_url,
                callback=self.parse_news,
                meta={'id': news_id, 'category': category}
            )

    def parse_news(self, response: Response, **kwargs):
        news = Selector(response).xpath('//div[@class="sidebar-1"]')

        item = VnExpressItem()
        item['_id'] = response.meta.get('id')
        item['source'] = self.name
        item['url'] = response.url
        item['category'] = CATEGORIES[response.meta.get('category')]
        item['title'] = self.extract_title(news)
        item['datetime'] = self.extract_datetime(news)
        item['abstract'] = self.extract_abstract(news)
        item['content'] = self.extract_content(news)
        item['author'] = self.extract_author(news)

        yield item

    
    #######################
    ## EXTRACT FROM NEWS ##
    #######################

    def extract_id(self, url: str):
        try:
            elements = url.split('/')
            elements = elements[-1].split('-')
            return elements[-1].replace('.html', '')
        except:
            return None

    
    def extract_title(self, news: Selector):
        try:
            title_data = news.xpath(
                '//h1[@class="title-detail"]/text()'
            ).extract()[0]
            return title_data
        except:
            return None

    def extract_datetime(self, news: Selector):
        try:
            datetime_data = news.xpath(
                '//div[@class="header-content width_common"]/span[@class="date"]/text()'
            ).extract()[0]
            return datetime_data
        except:
            return None

    def extract_abstract(self, news: Selector):
        try:
            abstract_data = news.xpath(
                '//p[@class="description"]/text()'
            ).extract()
            return '\n'.join(abstract_data)
        except:
            return None

    def extract_content(self, news: Selector):
        try:
            content_data = news.xpath(
                # '//article[@class="fck_detail "]//p[not(@class="Image")]//text()[normalize-space()]'
                '//article[@class="fck_detail "]//p[@class="Normal"]/text()'
            ).extract()

            return '\n'.join(content_data)
        except:
            return None

    def extract_author(self, news: Selector):
        try:
            author_data = news.xpath(
                '//article[@class="fck_detail"]/p[@class="Normal"][@style="text-align:right;"]/*/text()'
            ).extract()
            return author_data
        except:
            return None