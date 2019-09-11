# модуль для работы с сайтом superjob
from base import requestor
import requests
from pprint import pprint
import re
from bs4 import BeautifulSoup as bs

# создаем класс, который будет наследником базового класса
class superjob(requestor):
    def __init__(self):
        # а конструктор базовый класс не завещал, переинициализируем по-новому
        self.requestor = requestor()
        self.web_sj = 'https://www.superjob.ru/vacancy/search/'
        self.headers = self.requestor.headers
        self.paramsadditional = {}
        self.params = {}

    # Метод для подтверждения принятия параметров для get-запроса
    def applyparams(self,name_vac):
        self.params = {"keywords" : name_vac}

    # При поисковом запросе сайт меняет свой url. Данная функция позволяет "захватить" полученный url, с которым
    # будет работать в будущем
    def get_body(self, web, headers, params):
        page = requests.get(web, headers=headers, params=params)
        result = page.text
        # print(result)
        link = page.url
        # print('---')
        # print(link)
        # print('---')
        page.close()
        return link


    # функция скраппинга
    def get_vacs(self, web, headers, params):
        list_names = []
        list_links = []
        list_minzp = []
        list_maxzp = []
        list_sources = []
        source = 'SuperJob'
        # print(params)
        page_full = requests.get(web, headers=headers, params=params)
        # print(page_full.url)
        soup = bs(page_full.text, 'lxml')

        # Выбираем блок/столбец, где располагаются все вакансии
        block_vacs = soup.find('div', {'style': "display:block"}).findChildren(recursive=False)
        # pprint(block_vacs)
        # print('--------')

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
            # pprint(vac_names.getText())
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
                # print(zp[0])
                minzp = zp[0]
                maxzp = ''
                list_minzp.append(minzp)
                list_maxzp.append(maxzp)
            else:
                try:
                    minzp = zp[0].getText().replace('\xa0', '')
                    maxzp = zp[2].getText().replace('\xa0', '')
                    # print(zp[0].getText(), zp[2].getText())
                    list_minzp.append(minzp)
                    list_maxzp.append(maxzp)
                except IndexError:
                    minzp = zp[0].getText().replace('\xa0', '')
                    maxzp = ''
                    # print(zp[0].getText())
                    list_minzp.append(minzp)
                    list_maxzp.append(maxzp)
        return list_names, list_links, list_minzp, list_maxzp, list_sources

    # объединяем полученные из скрапинга списки в общие списки для формирования их в датафрейм
    def form_lists(self, num_pages):
        # print(blocki)
        url = self.get_body(self.web_sj, self.headers, self.params)

        names = []
        linki = []
        mins = []
        maxs = []
        istochniki = []
        self.web_sj = url

        try:
            for num_page in num_pages:
                self.params = {"page": str(num_page)}
                print('SJ: читаю страницу {}'.format(num_page))
                name, vlink, min, max, istochnik = self.get_vacs(self.web_sj, self.headers, self.params)
                names = names + name
                linki = linki + vlink
                mins = mins + min
                maxs = maxs + max
                istochniki = istochniki + istochnik
                # istochniki_ser = np.array(istochniki_ser, istochnik)
        except AttributeError:
            print('Чтение окончено')
            pass
        df = self.create_dataframe(names, linki, mins, maxs, istochniki)
        return df
