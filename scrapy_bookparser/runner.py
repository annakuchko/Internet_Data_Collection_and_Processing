from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from bookparser.spiders.labru import LabruSpider
from bookparser.spiders.bookru import BookruSpider
from bookparser import settings

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    
    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(LabruSpider)
    process.crawl(BookruSpider)
    
    process.start()
    