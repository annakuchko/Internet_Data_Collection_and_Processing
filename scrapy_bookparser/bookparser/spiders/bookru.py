import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class BookruSpider(scrapy.Spider):
    name = 'bookru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/knigi-bestsellery']
       
    def parse(self, response: HtmlResponse):
        print(response.url)
        book_links = response.xpath(
            '//*[contains(@class, "title-link")]/@href'
            ).extract()
        for link in book_links:
            link = f'https://book24.ru{link}'
            print(link)
            yield response.follow(link, callback=self.parse_books)
            
        next_page = response.xpath(
            '//*[contains(text(), "Далее")]/@href'
            ).get()
        
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        pass
    
    def parse_books(self, response: HtmlResponse):
        print('$$')
        title = response.xpath(
            '//*[contains(@itemprop, "name")]/text()'
            ).extract()[0]
        print(title)
        authors = response.xpath(
            '//*[contains(text(), "Автор:")]/parent::*//a/text()'
            ).extract()[0]
        print(authors)
        url = response.url
        try:
            new_price = response.xpath(
                '//*[contains(@itemprop, "price")]/text()'
                ).extract()[0]
        except:
            new_price = None
        print('New price: ', new_price)
        try:
            old_price = response.xpath(
                '//*[contains(@class, "prices")]//*'
                '[contains(@class, "price-old")]/text())'
                ).extract()
        except:
            old_price = None
        print('Old price:', old_price)
        book_rating = response.xpath(
            '//*[contains(@class, "rating__rate")]/text()'
            ).extract()[0]
        print('Rating: ', book_rating)
        
        yield BookparserItem(title = title, 
                             authors = authors,
                             url = url,
                             new_price = new_price,
                             old_price = old_price,
                             book_rating = book_rating)
        pass
