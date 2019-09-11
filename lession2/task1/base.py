# базовый класс для ХХ и супержлоба
import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import re

class requestor:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.71"}
        print('Успех')

    def create_dataframe(self, names, linki, mins, maxs, istochniki):
        dataframe_na_export = pd.DataFrame(list(zip(names, linki, mins, maxs, istochniki)), columns=['Имя', 'Ссылка',
                                                                                                     'Мин. зп',
                                                                                                     'Макс. зп',
                                                                                                     'Источник'])
        return dataframe_na_export

    def export_to_excel(self, dataframe1, dataframe2):
        result = pd.concat([dataframe1, dataframe2])
        result.to_excel('report.xlsx', index=False)

    def letsroll(self):
        self.params = {**self.params, **self.paramsadditional}


if __name__ == '__main__':
   print('zaglushko')
   '''
# Делаем реквест

    zaproshh = headhunter(paramshh)


    names, linki, mins, maxs, istochniki = zaproshh.form_list_hh(num_pages)
    reporthh = zaproshh.create_dataframe(names, linki, mins, maxs, istochniki)

    pprint(reporthh.head(25))

'''

'''  
# Методы НН    
    zaproshh = headhunter(params)
    
    names, linki, mins, maxs, istochniki = zaproshh.form_list(num_pages)
    reporthh = zaproshh.create_dataframe(names, linki, mins, maxs, istochniki)
'''

        # istochniki_ser = np.array(istochniki_ser, istochnik)
'''
# Методы для супержабы
    zapros = superjob(headers, params)

    imena, ssylki, miny, maxy, sourcey = zapros.form_lists()
    zapros.create_dataframe(imena, ssylki, miny, maxy, sourcey)



# TODO: сделать метод для экспорта в эйчтимиэль файл
    
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