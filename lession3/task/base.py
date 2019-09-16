# базовый класс для наших сценариев
import pandas as pd
from pymongo import MongoClient

class requestor:
    # Конструктор. Берем заголовки, они для обоих классов одинаковы
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.71"}

    # Функция создания датафрейма из кучи списков. Нужно для экспорта в Эксель
    def create_dataframe(self, names, linki, mins, maxs, istochniki):
        dataframe_na_export = pd.DataFrame(list(zip(names, linki, mins, maxs, istochniki)), columns=['Имя', 'Ссылка',
                                                                                                     'Мин. зп',
                                                                                                     'Макс. зп',
                                                                                                     'Источник'])
        return dataframe_na_export

    # Функция экспорта в эксель. На вход подаются пандовские датафреймы
    def export_to_excel(self, dataframe1, dataframe2):
        result = pd.concat([dataframe1, dataframe2])
        result.to_excel('report.xlsx', index=False)
        print('Файл {} получен!'.format('report.xlsx'))

    # По ходу скрапинга будут приходить новые параметры для get-запроса. Эта функция мёржит текущий словарь запросов с
    # вновь прибывшим
    def letsroll(self):
        self.params = {**self.params, **self.paramsadditional}

    def inserttomonga(self, name_vac, names, linki, mins, maxs, istochniki):
        client = MongoClient('localhost', 27017)
        db = client.vacancy
        col = db[name_vac]

        # print(type(new_posts))
        # # raise Exception

        dic = {"name": None, "linka": None, "min": None, "max": None, "source": None}
        total_list = list()
        for l1, l2, l3, l4, l5 in zip(names, linki, mins, maxs, istochniki):
            dic["name"] = l1
            dic["linka"] = l2
            if l3 == 'Не указано' or l3 == '':
                l3 = 0
                dic["min"] = int(l3)
            else:
                dic["min"] = int(l3)
            if l4 == '':
                l4 = 0
                dic["max"] = int(l4)
            else:
                dic["max"] = int(l4)
            dic["source"] = l5
            # print(dic)
            total_list.append(dic.copy())
        print(total_list)

        col.insert_many(total_list)


# Заглушка до лучших времен
if __name__ == '__main__':
   print('zaglushko')