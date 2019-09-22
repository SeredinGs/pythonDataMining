# модуль для работы с headhunter-om
from base import requestor
import re
import requests
from bs4 import BeautifulSoup as bs
import time

# создаем класс, который будет наследником базового класса
class headhunter(requestor):
    def __init__(self):
        # а конструктор базовый класс не завещал, переинициализируем по-новому
        self.requestor = requestor()
        self.web_hh = 'https://hh.ru/search/vacancy?'
        self.paramsadditional = {}
        self.params = {}
        self.headers = self.requestor.headers

    # Метод для подтверждения принятия параметров для get-запроса
    def applyparams(self, name_vac):
        self.params = {"L_is_autosearch": "false", "area": "1", "clusters": "true", "text": name_vac}

    # функция для запроса содержимого страницы. возвращает итоговую ссылку и содержимое
    def get_body_hh(self,params):
        page = requests.get(self.web_hh, headers=self.headers, params=params)
        result = page.text
        #pprint(result)
        link = page.url
        # print(page.headers)
        # print(link)
        return link, result

    # формирование общих списоков и создание датафрейма
    def form_list_hh(self, num_pages):
        names = []
        linki = []
        mins = []
        maxs = []
        istochniki = []

        # try:
        for page in num_pages:
            self.paramsadditional = {"page": page}
            self.letsroll()
            print('HH: читаю страницу {}'.format(page))
            url, body = self.get_body_hh(self.params)
            name, vlink, min, max, istochnik = self.get_vacs_HH(body)
            names = names + name
            linki = linki + vlink
            mins = mins + min
            maxs = maxs + max
            istochniki = istochniki + istochnik
        return self.create_dataframe(names, linki, mins, maxs, istochniki)

    # формирование общих списоков и для экспорта в монгу
    def form_list_hh_monga(self, num_pages):
        names = []
        linki = []
        mins = []
        maxs = []
        istochniki = []

        # try:
        for page in num_pages:
            self.paramsadditional = {"page": page}
            self.letsroll()
            print('HH: читаю страницу {}'.format(page))
            url, body = self.get_body_hh(self.params)
            name, vlink, min, max, istochnik = self.get_vacs_HH(body)
            names = names + name
            linki = linki + vlink
            mins = mins + min
            maxs = maxs + max
            istochniki = istochniki + istochnik
        return names, linki, mins, maxs, istochniki

    # функция для скрапинга страницы. Ставим слипы для подстраховки
    def get_vacs_HH(self, page):
        time.sleep(5)
        list_names = []
        list_links = []
        list_minzp = []
        list_maxzp = []
        list_sources = []
        source = 'HH'
        soup = bs(page, 'lxml')

        block_vacs = soup.find('div', {'class': 'vacancy-serp'})

        for vac in block_vacs:
            list_sources.append(source)
            head = vac.find('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
            if head is None:
                continue
            # pprint(head)
            a = head.find('a')
            # pprint(a)
            # Имя
            list_names.append(a.getText())
            # pprint(a.getText())
            # Линка
            list_links.append(a['href'])
            # pprint(a['href'])
            zp = vac.find('div', {'class': 'vacancy-serp-item__compensation'})
            if zp is None:
                minzp = 'Не указано'
                maxzp = ''
                list_minzp.append(minzp)
                list_maxzp.append(maxzp)
                # print(minzp, maxzp)
                continue
            zp_full = zp.getText().replace('\xa0', '')
            # print(zp_full)
            if zp_full[0:2] == 'от':
                # print('first')
                # print(re.findall('\d*', zp_full))
                minzp = re.findall('\d*', zp_full)[3]
                maxzp = ''
                list_minzp.append(minzp)
                list_maxzp.append(maxzp)
                # print(minzp, maxzp)
            elif zp_full[0:2] == 'до':
                minzp = ''
                # print('second')
                # print(re.findall('\d*', zp_full)[3])
                maxzp = re.findall('\d*', zp_full)[3]
                list_minzp.append(minzp)
                list_maxzp.append(maxzp)
                # print(minzp, maxzp)
            else:
                list_zp = re.split('\-', zp_full)
                # print('third')
                minzp = list_zp[0]
                maxzp = re.match('\d*',list_zp[1]).group(0)
                list_minzp.append(minzp)
                list_maxzp.append(maxzp)
                # print(minzp, maxzp)
        return list_names, list_links, list_minzp, list_maxzp, list_sources
