import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import pandas as pd
import numpy as np


# Делаем реквест

def get_body(address, headers, params):
    page = requests.get(address, headers=headers, params=params)
    result = page.text
    pprint(result)
    link = page.url
    #print(page.headers)
    #print(link)
    return link, result

### ХХ
def get_vacs_HH(page):
    list_names = []
    list_links = []
    list_minzp = []
    list_maxzp = []
    list_sources = []
    source = 'HH'
    soup = bs(page, 'lxml')

    block_vacs = soup.find('div', {'class' : 'vacancy-serp'})

    for vac in block_vacs:
        list_sources.append(source)
        head = vac.find('div', { 'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
        if head is None:
            continue
        #pprint(head)
        a = head.find('a')
        #pprint(a)
        # Имя
        list_names.append(a.getText())
        #pprint(a.getText())
        # Линка
        list_links.append(a['href'])
        #pprint(a['href'])
        zp = vac.find ('div', { 'class' : 'vacancy-serp-item__compensation'})
        if zp is None:
            minzp = 'Не указано'
            maxzp = ''
            list_minzp.append(minzp)
            list_maxzp.append(maxzp)
            # print(minzp, maxzp)
            continue
        zp_full = zp.getText().replace('\xa0','')
        #print(zp_full)
        if zp_full[0:2] == 'от':
            minzp = re.findall('\d*', zp_full)[3]
            maxzp = ''
            list_minzp.append(minzp)
            list_maxzp.append(maxzp)
            # print(minzp, maxzp)
        elif zp_full[0:2] == 'до':
            minzp = ''
            maxzp = re.findall('\d*', zp_full)[3]
            list_minzp.append(minzp)
            list_maxzp.append(maxzp)
            # print(minzp, maxzp)
        else:
            list_zp = re.split('\-', zp_full)
            minzp = list_zp[0]
            maxzp = list_zp[1]
            list_minzp.append(minzp)
            list_maxzp.append(maxzp)
            # print(minzp, maxzp)
    return list_names, list_links, list_minzp, list_maxzp, list_sources


# Подготовка
name_vac = 'стажер'
pages= list('1,2,3,4,5')
num_pages = [pages[x] for x in range(0, len(pages), 2)]
address = 'https://hh.ru/search/vacancy'
list_num=[]
headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.71"}

names = []
linki = []
mins = []
maxs = []
istochniki = []

#try:
for page in num_pages:
    params = {"L_is_autosearch": "false", "area": "1", "clusters": "true", "text": name_vac, "page": page}
    url, body = get_body(address, headers, params)
    name, vlink, min, max, istochnik = get_vacs_HH(body)
    names = names+name
    linki = linki+vlink
    mins = mins + min
    maxs = maxs + max
    istochniki = istochniki + istochnik
    #istochniki_ser = np.array(istochniki_ser, istochnik)
'''
except AttributeError:
    print('Больше страниц нет. Отбой!')
    pass
'''
dataframe_na_export = pd.DataFrame(list(zip(names, linki, mins, maxs, istochniki)), columns=['Имя', 'Ссылка',
                                                                                             'Мин. зп','Макс. зп',
                                                                                             'Источник'])
dataframe_na_export.to_excel('output1.xlsx')

#print(num_pages)




# print(names)
# print(linki)
# print(mins)
# print(maxs)
# print(istochniki)


# address = 'https://www.superjob.ru/vacancy/search/?keywords='.encode('utf-8')



# https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=стажер&page=1


# https://www.superjob.ru/vakansii/stazher.html?page=2

# https://www.superjob.ru/vacancy/search/?keywords=datascientist