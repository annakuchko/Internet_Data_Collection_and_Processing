import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabruSpider(scrapy.Spider):
    name = 'labru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/books/']
       
    def parse(self, response: HtmlResponse):
        print(response.url)
        book_links = response.xpath(
            '//*[contains(@class, "title-link")]/@href'
            ).extract()
        for link in book_links:
            link = f'https://www.labirint.ru{link}'
            print(link)
            yield response.follow(link, callback=self.parse_books)
            
        next_page = response.xpath(
            '//*[contains(text(), "Следующая")]/@href'
            )[0].get()
        
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_books(self, response: HtmlResponse):
        title = response.xpath(
            '//*[contains(@id, "title")]//h1/text()'
            ).extract()[0]
        print(title)
        try:
            authors = response.xpath(
                '//*[contains(text(), "Автор:")]/a/text()'
                ).extract()[0]
        except:
            authors = None
        print(authors)
        url = response.url
        try:
            new_price = response.xpath(
                '//span[contains(@class, "pricenew-val-number")]/text()'
                ).extract()[0]
        except:
            new_price = None
        print('New price: ', new_price)
        try:
            old_price = response.xpath(
                '//span[contains(@class, "priceold")]/text()'
                ).extract()[0]
        except:
            old_price = None
        print('Old price:', old_price)
        book_rating = response.xpath(
            '//*[contains(text(), "Рейтинг")]/child::*/text()'
            ).extract()[0]
        print('Rating: ', book_rating)
        
        yield BookparserItem(title=title, 
                             authors=authors,
                             url=url,
                             new_price=new_price,
                             old_price=old_price,
                             book_rating=book_rating)

