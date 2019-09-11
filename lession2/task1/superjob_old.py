from pprint import pprint
import re
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from base import superjob as ss

# Подготовка
name_vac = 'кассир'

address = 'https://www.superjob.ru/vacancy/search/'
list_num=[]
pages= list('1,2,3,4,5')
num_pages = [pages[x] for x in range(0, len(pages), 2)]
print(num_pages)

# Делаем реквест
sj = ss()

headers = sj.headers
address = sj.web_sj
sj.params = params

def get_body(web, headers, params):
    page = requests.get(web, headers=headers, params=params)
    result = page.text
    #print(result)
    link = page.url
    print('---')
    print(link)
    print('---')
    page.close()
    return link

'''
file = open('output.html','w+', encoding='utf-8')
file.write(result)
file.close()
'''
# делаем из неё суп(Супер Жоб)
def get_vacs(link):
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
    block_vacs = soup.find('div', {'style' : "display:block"}).findChildren(recursive=False)
    #pprint(block_vacs)
    print('--------')

    # Парсим нужные нам значения.
    # Не забываем о проверке содержимого на пустые множества и None-ы

    for vac in block_vacs:
        list_sources.append(source)
        vacansii = vac.findAll('div', { "class" : "_2g1F-"})
        #pprint(vacancii)
        if len(vacansii) == 0:
            continue
        vac_names = vacansii[0].find('a', {'target' : "_blank"})
        if vac_names is None:
            continue
        # Ссылка на вакансию
        vac_link = 'http://www.superjob.ru'+vac_names['href']
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
        span = vac.findAll('span', { 'class': re.compile('f-test-text-company-item-salary')})
        #pprint(span)
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
                minzp = zp[0].getText().replace('\xa0','')
                maxzp = zp[2].getText().replace('\xa0','')
                print(zp[0].getText(), zp[2].getText())
                list_minzp.append(minzp)
                list_maxzp.append(maxzp)
            except IndexError:
                minzp = zp[0].getText().replace('\xa0','')
                maxzp = ''
                print(zp[0].getText())
                list_minzp.append(minzp)
                list_maxzp.append(maxzp)
    return list_names, list_links, list_minzp, list_maxzp, list_sources

#print(blocki)
url = get_body(address, headers, params)
links = [url[0:-19]+'page='+x for x in num_pages]
print(links)

names = []
linki = []
mins = []
maxs = []
istochniki = []


try:
    for link in links:
        name, vlink, min, max, istochnik = get_vacs(link)
        names = names+name
        linki = linki+vlink
        mins = mins + min
        maxs = maxs + max
        istochniki = istochniki + istochnik
        #istochniki_ser = np.array(istochniki_ser, istochnik)
except AttributeError:
    print('Больше страниц нет. Отбой!')
    pass

dataframe_na_export = pd.DataFrame(list(zip(names, linki, mins, maxs, istochniki)), columns=['Имя', 'Ссылка',
                                                                                             'Мин. зп','Макс. зп',
                                                                                             'Источник'])
dataframe_na_export2 = pd.DataFrame(list(zip(names, linki, mins, maxs, istochniki)), columns=['Имя', 'Ссылка',
                                                                                             'Мин. зп','Макс. зп',
                                                                                             'Источник'])
superjob = ss({})

superjob.export_to_excel(dataframe_na_export,dataframe_na_export2)