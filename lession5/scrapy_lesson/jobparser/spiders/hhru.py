# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import re


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=python&area=113&st=searchVacancy']
# заметил фичу: если текст в параметре text совпадает с частью имени в вакансии, то этот текст захватывается в отдельный span

    def parse(self, response: HtmlResponse):  # Метод парсинга - точка входа для паука
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()  # Ссылка у кнопки "Далее"
        yield response.follow(next_page, callback=self.parse)  # Переход на следующую страницу и вызов самой себя
        # Как только дошли до последней страницы идем дальше по коду
        vacancy = response.css(  # Ищем ссылку на вакансию и добавляем ее в наш список
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()

        for link in vacancy:  # Переходим по ссылкам на вакансии из полученного списка
            yield response.follow(link, callback=self.vacansy_parse)  # Вызываем метод для сбора инф-ции со страницы

    def vacansy_parse(self, response: HtmlResponse):
        name_vac = ''
        name1 = response.css('div.vacancy-title h1.header span.highlighted::text').getall()  # Наименование вакансии
        name2 = response.css('div.vacancy-title h1.header::text').extract_first() # HH добавили...
        if len(name1) == 0: # ...в заголовок имени span, приходится добавлять новые обработчики и соответственно проверки
            if name2 is not None:
                name_vac = name2
        else:
            if name2 is None:
                name_vac = name1
            else:
                name_vac = name1[0] + name2
        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract_first()  # Зарплата
        min_sal, max_sal = self.parse_salara(salary)
        url = response.url
        # Сделаем примитивный вывод для показывающий результат
        #print('name = {}, salary = {}, min_sal = {}, max_sal = {}, url = {}'.format(name, salary, min_sal, max_sal, url))
        yield JobparserItem(name=name_vac, min_salary=min_sal, max_salary=max_sal, link=url, source='HH')  # Передаем сформированный item в pipeline

    # поскольку в конвейер(пайплайн) приходят уже готовые результаты, оставляем это на совесть пауку
    # ВОПРОС: где этично размещать обработку?
    def parse_salara(self, salary):
        print('-ЗП ПРИШЛА-')
        print(salary)
        print('-----------')
        if salary == ' з/п не указана':
            minzp = 'Не указано'
            maxzp = None
        else:
            salary = salary.replace('\xa0', '')
            # только ОТ
            if (salary[0:2] == 'от' and re.search(r'до.\d', salary) == None):
                # print('first')
                # print(re.findall('\d*', salary))
                minzp = re.findall('\d*', salary)[3]
                maxzp = None
                # print(minzp, maxzp)
            # только ДО
            elif salary[0:2] == 'до':
                minzp = None
                # print('second')
                # print(re.findall('\d*', salary)[3])
                maxzp = re.findall('\d*', salary)[3]
                # print(minzp, maxzp)
            # только ОТ и ДО
            else:
                list_zp = re.split('до', salary)
                # print('third')
                minzp = list_zp[0].replace('от ', '')
                minzp = re.search('\d*', minzp).group(0)
                maxzp = list_zp[1].replace(' ', '')
                maxzp = re.match(r'\d*', maxzp).group(0)
                print('')
        return minzp, maxzp
