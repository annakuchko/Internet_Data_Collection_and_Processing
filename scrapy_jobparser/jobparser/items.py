import scrapy


class JobparserItem(scrapy.Item):
    
    _id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    salary_max = scrapy.Field()
    salary_min = scrapy.Field()
    url = scrapy.Field()
    
    pass
