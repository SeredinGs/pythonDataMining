# класс чтения икспассов с определенных сайтов
from base import requestor
import requests
from pprint import pprint
from lxml import html
from datetime import datetime
import re

class xpathman(requestor):
    def __init__(self):
        self.list_sites = ['http://www.yandex.ru/', 'https://news.mail.ru', 'http://lenta.ru']
    # на стартовой странице Яндекса имеется дата, время и главные новости. на спец-страницу с новостями переходить НЕ
    # нужно
    def get_news_ya(self):
        site = self.list_sites[0]
        req = requests.get(site)
        result = html.fromstring(req.text)
        text = result.xpath("//div[@id='news_panel_news']/*/*/a/span/span[@class='news__item-content']/text()")
        href = result.xpath(".//div[@id='news_panel_news']/*/*/a/@href")
        day = result.xpath(".//span[contains(@class,'datetime__day')]/text()")
        month = result.xpath(".//span[contains(@class,'datetime__month')]/text()")
        day_of_week = result.xpath(".//span[contains(@class,'datetime__wday')]/text()")
        hour = result.xpath(".//span[contains(@class,'datetime__hour')]/text()")
        min = result.xpath(".//span[contains(@class,'datetime__min')]/text()")
        time = day[0]+' '+month[0]+' '+day_of_week[0]+' '+hour[0]+':'+min[0]
        pprint('----------------------------')
        pprint('Новости от {}'.format(site))
        pprint('На {}'.format(time))
        pprint('----------------------------')
        for name,link in zip(text,href):
            pprint(name)
            pprint(link)
    # На стартовой странице mail нет текущей даты и времени, поэтому воспользуемся спец страницей. В качестве времени
    # воспользуемся функцией datetime
    def get_news_mail(self):
        site = self.list_sites[1]
        req = requests.get(site)
        result = html.fromstring(req.text)
        text = result.xpath(".//ul[@name='clb20268353']/*/a/text()")
        href = result.xpath(".//ul[@name='clb20268353']/*/a/@href")
        pprint('----------------------------')
        pprint('Новости от {} на'.format(site))
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string)
        pprint('----------------------------')
        for name, link in zip(text, href):
            pprint(name.replace('\xa0', ' '))
            # среди новостей пролетали ссылки с полным УРЛ. Удалось поймать такое только для спортивных новостей
            if re.search(r'sportmail.', link) is not None:
                pprint(link)
            else:
            # в остальных случаях складываем 2 части
                pprint(site+link)
    # у ленты все просто, заголовки, ссылки и даты в одном месте с новостями, поэтому в титульный экран даты входить
    # не будут
    def get_news_lenta(self):
        site = self.list_sites[2]
        req = requests.get(site)
        result = html.fromstring(req.text)
        text = result.xpath(".//section[@class='row b-top7-for-main js-top-seven']//a[not(@class)]/text()")
        href = result.xpath(".//section[@class='row b-top7-for-main js-top-seven']//a[not(@class)]/@href")
        dates = result.xpath(".//section[@class='row b-top7-for-main js-top-seven']//a[not(@class)]/time/@title")
        times = result.xpath(".//section[@class='row b-top7-for-main js-top-seven']//a[not(@class)]/time/text()")
        pprint('----------------------------')
        pprint('Новости от {}'.format(site))
        pprint('----------------------------')
        for name, link, date, time in zip(text, href, dates, times):
            pprint(date+' '+time)
            pprint(name.replace('\xa0', ' '))
            pprint(site+link)


if __name__ == '__main__':
    xp = xpathman()
    xp.get_news_ya()
    xp.get_news_lenta()
    xp.get_news_mail()