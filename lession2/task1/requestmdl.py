import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import pandas as pd
import numpy as np

### Супер-Жоб
'''
# Подготовка
name_vac = 'программист'
vac_utf = name_vac.encode('utf-8')
address = 'https://www.superjob.ru/vacancy/search/?keywords='.encode('utf-8')
web = address + vac_utf
list_num=[]
pages= list('1,2,3,4,5')
num_pages = [pages[x] for x in range(0, len(pages), 2)]
print(num_pages)

# Делаем реквест
page = requests.get(web)
result = page.text
#print(result)
link = page.url

print(link)
page.close()

# Пишем в аштиэмэль
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
        vac_link = vac_names['href']
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
'''
#print(blocki)
links = [link[0:-19]+'page='+x for x in num_pages]
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
dataframe_na_export.to_excel('output.xlsx')
'''





# Делаем реквест

def get_body(address, headers, params):
    page = requests.get(address, headers=headers, params=params)
    result = page.text
    pprint(result)
    link = page.url
    #print(page.headers)
    #print(link)
    return link, result

# Пишем в аштиэмэль
"""
file = open('output1.html','w+', encoding='utf-8')
file.write(result)
file.close()
"""
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