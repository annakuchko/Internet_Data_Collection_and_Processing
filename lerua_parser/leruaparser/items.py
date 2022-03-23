# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose
import re

def clear_url(url):
    url = f'https://leroymerlin.ru{url}'
    return url

def get_big_img_url(url):
    url = url.replace('https', 'http')
    # url = re.sub(
    #     r'(upload/)([\s\S]*?)(/LMCode)',
    #     r'f_auto,q_90,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png',
    #     url
    #     )
    print(url)
    return url 

class LeruaparserItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field(input_processor=MapCompose(clear_url))
    photos = scrapy.Field(input_processor=MapCompose(get_big_img_url))
    params = scrapy.Field()
    price = scrapy.Field()
    _id = scrapy.Field()
