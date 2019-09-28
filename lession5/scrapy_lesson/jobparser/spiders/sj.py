# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import time

class SjSpider(scrapy.Spider):
    print('SJ запустился')
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python'] # имя вакансии вводим тут

    # Делаем всё аналогично hh, правда с xpath-ами, селекторы не сработали:
    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe']/@href").extract_first()
        if next_page != None:
            yield response.follow(next_page, callback=self.parse)
        else:
            pass
        vacancy = response.xpath('//div[@class="_2g1F-"]/a[@target="_blank"]/@href').extract()
        for link in vacancy:  # Переходим по ссылкам на вакансии из полученного списка
            yield response.follow(link, callback=self.vacansy_parse)  # Вызываем метод для сбора инф-ции со страницы
        #print(next_page[0])
        pass


    def vacansy_parse(self, response: HtmlResponse):
        #time.sleep(5)
        name = response.xpath('//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]/text()').extract()
        name_vac = name[0]
        # zp = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]')
        zp = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]/span/text()').extract()
        if len(zp) == 0:
            min_sal ='Не указано'
            max_sal = None
        elif len(zp) == 2:
            min_sal = zp[0]
            max_sal = None
        else:
            min_sal = zp[0]
            max_sal = zp[2]

        url = response.url
        # Сделаем примитивный вывод показывающий результат
        print('name = {}, salary = {}, min_sal = {}, max_sal = {}, url = {}'.format(name, zp, min_sal, max_sal, url))
        yield JobparserItem(name=name_vac, min_salary=min_sal, max_salary=max_sal, link=url,
                            source='SJ')  # Передаем сформированный item в pipeline
