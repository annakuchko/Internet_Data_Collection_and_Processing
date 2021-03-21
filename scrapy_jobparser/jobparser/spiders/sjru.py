import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/analitik.html']

    def start_requests(self):
        urls = self.start_urls
        
        for url in urls:
            req= scrapy.Request(url=url, callback=self.parse)
            req.headers['Cookie'] = 'js_enabled=true; is_cookie_active=true;'
            yield req
            
    def parse(self, response: HtmlResponse):
        print(response.url)
        vacancy_links = response.xpath(
            '//div[contains(@class, "vacancy-item")]//'
            'a[not(contains(@href, "clients"))]/@href'
            ).extract()
        for link in vacancy_links:
            print(link)
            yield response.follow(link, callback=self.parse_vacancies)
            
        next_page = response.xpath(
            '//*[contains(@class, "Dalshe")]/@href'
            ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        pass
    
    def parse_vacancies(self, response: HtmlResponse):
        title = response.xpath(
            "//h1/text()"
            ).extract()
        salary = response.xpath(
            '//*[contains(@class, "_1OuF_ ZON4b")]//text()'
            ).extract()
        url = response.url
        yield JobparserItem(title = title, salary = salary, url = url)
        pass
        