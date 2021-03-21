import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://samara.hh.ru/vacancies/analyst']

    def start_requests(self):
        urls = self.start_urls
        
        for url in urls:
            req= scrapy.Request(url=url, callback=self.parse)
            req.headers['Cookie'] = 'js_enabled=true; is_cookie_active=true;'
            yield req
            
    def parse(self, response: HtmlResponse):
        print(response.url)
        vacancy_links = response.xpath(
            '//*[contains(@class, "vacancy-serp-item")]//*[contains(@data-qa,'
            ' "title")]/@href'
            ).extract()
        for link in vacancy_links:
            print(link)
            yield response.follow(link, callback=self.parse_vacancies)
            
        next_page = response.xpath(
            '//*[contains(@data-qa, "pager-next")]/@href'
            ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        pass
    
    def parse_vacancies(self, response: HtmlResponse):
        title = response.xpath(
            "//*[contains(@class, 'vacancy-title')]//h1//text()"
            ).extract()
        salary = response.xpath(
            "//*[contains(@class, 'vacancy-salary')]/span/text()"
            ).extract()
        url = response.url
        
        yield JobparserItem(title = title, salary = salary, url = url)
        pass
        
