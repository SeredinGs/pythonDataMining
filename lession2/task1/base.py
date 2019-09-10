# базовый класс для ХХ и супержлоба
import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import re

class requestor:
    def __init__(self, zagolovok, param):
        self.headers = zagolovok
        self.params = param
        print('Успех')

    def create_dataframe(self, names, linki, mins, maxs, istochniki):
        dataframe_na_export = pd.DataFrame(list(zip(names, linki, mins, maxs, istochniki)), columns=['Имя', 'Ссылка',
                                                                                                     'Мин. зп',
                                                                                                     'Макс. зп',
                                                                                                     'Источник'])
        dataframe_na_export.to_excel('itogoviy.xlsx', index=False)
        return dataframe_na_export

    def export_to_excel(self, dataframe1, dataframe2):
        result = pd.concat([dataframe1, dataframe2])
        result.to_excel('report.xlsx')

class superjob(requestor):
    def __init__(self, zagolovok, param):
        self.web_sj = 'https://www.superjob.ru/vacancy/search/'
        self.headers = zagolovok
        self.params = param
        print('Успех')

    def form_lists(self):
        url = self.get_body(self.web_sj, self.headers, self.params)
        links = [url[0:-19] + 'page=' + x for x in num_pages]
        print(links)

        names = []
        linki = []
        mins = []
        maxs = []
        istochniki = []

        try:
            for link in links:
                name, vlink, min, max, istochnik = self.get_vacs(link)
                names = names + name
                linki = linki + vlink
                mins = mins + min
                maxs = maxs + max
                istochniki = istochniki + istochnik
                # istochniki_ser = np.array(istochniki_ser, istochnik)
        except AttributeError:
            print('Больше страниц нет. Отбой!')
            pass
        return names,linki,mins,maxs,istochniki

    # Делаем реквест
    def get_body(self, web_sj, headers, params):
        page = requests.get(web_sj, headers=headers, params=params)
        result = page.text
        # print(result)
        link = page.url
        print(link)
        page.close()
        return link

    # делаем из неё суп(Супер Жоб)
    def get_vacs(self,link):
        list_names = []
        list_links = []
        list_minzp = []
        list_maxzp = []
        list_sources = []
        source = 'SuperJob'
        print(link)
        page_full = requests.get(link)
        soup = bs(page_full.text, 'lxml')

        # Выбираем блок/столбец, где располагаются все вакансии
        block_vacs = soup.find('div', {'style': "display:block"}).findChildren(recursive=False)
        # pprint(block_vacs)
        print('--------')

        # Парсим нужные нам значения.
        # Не забываем о проверке содержимого на пустые множества и None-ы

        for vac in block_vacs:
            list_sources.append(source)
            vacansii = vac.findAll('div', {"class": "_2g1F-"})
            # pprint(vacancii)
            if len(vacansii) == 0:
                continue
            vac_names = vacansii[0].find('a', {'target': "_blank"})
            if vac_names is None:
                continue
            # Ссылка на вакансию
            vac_link = 'http://www.superjob.ru' + vac_names['href']
            list_links.append(vac_link)
            # Имя вакансии
            pprint(vac_names.getText())
            vac_name = vac_names.getText()
            list_names.append(vac_name)

            # В случае c зарплатой наблюдается 3 варианта:
            # а) Известны мин и макс значения
            # б) Известнен только мин
            # в) Не указано
            # Для этого пришлось вводить блок проверки
            span = vac.findAll('span', {'class': re.compile('f-test-text-company-item-salary')})
            # pprint(span)
            zp = span[0].findChildren()
            # pprint(zp)
            if zp == []:
                zp.append('Не указано')
                print(zp[0])
                minzp = zp[0]
                maxzp = ''
                list_minzp.append(minzp)
                list_maxzp.append(maxzp)
            else:
                try:
                    minzp = zp[0].getText().replace('\xa0', '')
                    maxzp = zp[2].getText().replace('\xa0', '')
                    print(zp[0].getText(), zp[2].getText())
                    list_minzp.append(minzp)
                    list_maxzp.append(maxzp)
                except IndexError:
                    minzp = zp[0].getText().replace('\xa0', '')
                    maxzp = ''
                    print(zp[0].getText())
                    list_minzp.append(minzp)
                    list_maxzp.append(maxzp)
        return list_names, list_links, list_minzp, list_maxzp, list_sources

class headhunter(requestor):
    def __init__(self, zagolovok, param):
        self.web_hh = 'https://hh.ru/search/vacancy'
        self.headers = zagolovok
        self.params = param
        print('Успех')




if __name__ == '__main__':

    name_vac = 'художник'
    list_num = []
    pages = list('1,2,3,4,5')
    num_pages = [pages[x] for x in range(0, len(pages), 2)]
    print(num_pages)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.71"}
    params = {"keywords": name_vac}

    zapros = superjob(headers, params)

    imena, ssylki, miny, maxy, sourcey = zapros.form_lists()
    zapros.create_dataframe(imena, ssylki, miny, maxy, sourcey)



# TODO: сделать метод для экспорта в эйчтимиэль файл
    '''
    file = open('output.html','w+', encoding='utf-8')
    file.write(result)
    file.close()
    '''

"""
Класс (профессия, страницы)
    дэф Конструктор
        ???

# у каждого будет своё
    дэф запрос_на_тело(профессия, страницы)
        ???
        Ретёрн боди

# у каждого будет своё
    дэф скраппинг(боди)
        ???
        Ретёрн листы(нэйм, линк, мин, макс, сурс)


    дэф форм_листс(страницы)
        Листы фулл
        фор и ин страницы:
            Листы_часть = скраппинг(запрос_на_тело())
            Листы_фулл = Листы_Фулл + Листы_часть
        ретёрн Листы_фулл


    дэф экспорт_у_эксел(Листы_фулл)
        Датафрейм
        Датафрейм_ту_эксел
"""