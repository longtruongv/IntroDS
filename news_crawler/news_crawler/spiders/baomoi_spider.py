from news_crawler.items import BaoMoiItem

import scrapy
from scrapy import Selector
from scrapy.http import Request, Response

from dateutil import parser

CATEGORIES = {
    'the-gioi': 'Thế giới',
    'xa-hoi': 'Xã hội',
    'van-hoa': 'Văn hóa',
    'kinh-te': 'Kinh tế',
    'giao-duc': 'Giáo dục',
    'the-thao': 'Thể thao',
    'giai-tri': 'Giải trí',
    'phap-luat': 'Pháp luật',
    'khoa-hoc-cong-nghe': 'Khoa học - Công nghệ',
    'khoa-hoc': 'Khoa học',
    'doi-song': 'Đời sống',
    'xe-co': 'Xe cộ',
    'nha-dat': 'Nhà đất',
    # 'suc-khoe-y-te': 'Sức khoẻ - Y tế',
    # 'du-lich': 'Du lịch'
}

class BaomoiSpider(scrapy.Spider):
    name = 'baomoi'
    based_url = 'https://baomoi.com'

    allowed_domains = ['baomoi.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        for category in CATEGORIES.keys():
            url = f'{self.based_url}/{category}.epi'
            yield Request(
                url=url,
                callback=self.parse_news_list,
                meta={'category': category},
            )


    def parse_news_list(self, response: Response, **kwargs):
        category = response.meta.get('category')
        news_list = Selector(response)

        news_uri_list = news_list.xpath('//div[@class="bm_OS bm_s"]//div[@class="bm_B"]//h4[@class="bm_G"]/span/a/@href').extract()
        for news_uri in news_uri_list:
            news_url = self.based_url + news_uri

            news_id = self.extract_id(news_url)
            if not news_id:
                continue

            yield Request(
                url=news_url,
                callback=self.parse_news,
                meta={'id': news_id, 'category': category}
            )


    def parse_news(self, response: Response, **kwargs):
        news = Selector(response)

        item = BaoMoiItem()
        item['_id'] = self.extract_id(response.meta.get('id'))
        item['url'] = response.url
        item['category'] = CATEGORIES[response.meta.get('category')]
        item['title'] = self.extract_title(news)
        item['datetime'] = self.extract_datetime(news)
        item['abstract'] = self.extract_abstract(news)
        item['content'] = self.extract_content(news)
        item['author'] = self.extract_author(news)
        item['keywords'] = self.extract_keywords(news)

        yield item


    #######################
    ## EXTRACT FROM NEWS ##
    #######################

    def extract_id(self, url: str):
        try:
            elements = url.split('/')
            return elements[-1].replace('.epi', '')
        except:
            return None

    def extract_title(self, news: Selector):
        try:
            title_data = news.xpath(
                '//h1[@class="bm_G"]/text()'
            ).extract()[0]
            return title_data
        except:
            return None


    def extract_datetime(self, news: Selector):
        try:
            datetime_data = news.xpath(
                '//div[@class="bm_AL"]/time/@datetime'
            ).extract()[0]
            datetime_data = parser.parse(datetime_data)
            return datetime_data
        except:
            return None


    def extract_abstract(self, news: Selector):
        try:
            abstract_data = news.xpath(
                '//h3[@class="bm_y bm_G"]/text()'
            ).extract()
            return '\n'.join(abstract_data)
        except:
            return None


    def extract_content(self, news: Selector):
        try:
            content_data = news.xpath(
                '//div[@class="bm_IM"]/p[@class="bm_BI"]/text()'
            ).extract()
            return '\n'.join(content_data)
        except:
            return None


    def extract_author(self, news: Selector):
        try:
            author_data = news.xpath(
                '//div[@class="bm_IM"]/p[@class="bm_BI bm_IP"]//text()'
            ).extract()[0]
            return author_data
        except:
            return None


    def extract_keywords(self, news: Selector):
        try:
            keywords_data  = news.xpath(
                '//div[@class="bm_OQ"]/ul/li[@class="bm_Cr"]/a/text()'
            ).extract()
            return keywords_data
        except:
            return None