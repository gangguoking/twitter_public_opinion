import scrapy


class TwitterSpider(scrapy.Spider):
    name = "twitter"
    allowed_domains = ["twitter.com"]
    start_urls = ["http://twitter.com/"]

    def parse(self, response):
        pass
