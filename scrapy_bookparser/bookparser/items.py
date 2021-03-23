# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    
    _id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    authors = scrapy.Field()
    new_price = scrapy.Field()
    old_price = scrapy.Field()
    book_rating = scrapy.Field()
