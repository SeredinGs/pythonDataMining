# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class PauchokSpider(scrapy.Spider):
    name = 'pauchok'
    allowed_domains = ['mvideo.ru']
    start_urls = ['http://mvideo.ru/']
    headers = {"adrum_0": "g:d3842ca6-ddd1-4b9f-a012-42dde53e31fd",
               "adrum_1": "n:customer1_b8e1f0e6-cc5b-4da4-a095-00a44385df2e",
               "adrum_2": "i:2695",
               "adrum_3": "e:57"}

    def parse(self, response:HtmlResponse):
        a = scrapy.http.request(url = self.start_urls[0], headers = self.headers)
        print('0')
        pass
