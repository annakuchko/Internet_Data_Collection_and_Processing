import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader

def clear_url(url):
    url = f'https://leroymerlin.ru{url}'
    return url

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru',
                       'res.cloudinary.com']

    def __init__(self, search):
        super(LeruaSpider, self).__init__()
        self.start_urls = [
            'https://leroymerlin.ru/search/?q={search}'
        ]

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            "//*[contains(@slot, 'picture')]/@href"
            ).extract()
        for link in links:
            yield response.follow(
                link, callback=self.parse_item
                )

        pass

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath("name", '//*[contains(@slot, "title")]/text()')
        loader.add_xpath("photos", '//*[contains(@slot, "pictures")]//@src')
        loader.add_xpath("price", '//*[contains(@slot, "price")]/text()')
        loader.add_xpath("params", '//*[contains(@class, "characteristicks")]'
                         '//*[contains(@class, "def-list")]/text()')
        yield loader.load_item()

