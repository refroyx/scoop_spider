# -*- coding: utf-8 -*-
import scrapy
from inscriptis import get_text

class ScooSpider(scrapy.Spider):
    name = 'scoo'
    allowed_domains = ['scoop.co.nz']
    start_urls = ['http://scoop.co.nz/']

    def start_requests(self):
        with open('input.txt') as f:
            urls = [line.strip() for line in f.readlines()]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.TextResponse):
        item = {}
        item['title'] = response.xpath('//div[@id="article"]/div/h1/text()').get()
        lines = response.xpath('//div[@id="article"]/div/following-sibling::*').getall()[2:]
        out=[]

        for line in lines:
            if line[3:].strip().startswith('By'):
                item['byline'] = line[3:-3]
                continue
            if line[3:].strip().startswith('(BusinessDesk)') or line[3:].strip().startswith('© Scoop Media'):
                break
            out.append(line)

        item['body'] = get_text(''.join(out))
        item['date'] = response.xpath('//span[@class="byline"]/b/text()').get()
        yield item