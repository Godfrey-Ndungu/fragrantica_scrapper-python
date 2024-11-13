import scrapy


class FragranticaSpider(scrapy.Spider):
    name = "fragrantica"
    allowed_domains = ["fragrantica.com"]
    start_urls = ["https://fragrantica.com"]

    def parse(self, response):
        pass
