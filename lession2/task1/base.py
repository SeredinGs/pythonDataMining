# базовый класс для наших сценариев
import pandas as pd

class requestor:
    # Конструктор. Берем заголовки, они для обоих классов одинаковы
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.71"}
        print('Успех')

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

    # По ходу скрапинга будут приходить новые параметры для get-запроса. Эта функция мёржит текущий словарь запросов с
    # вновь прибывшим
    def letsroll(self):
        self.params = {**self.params, **self.paramsadditional}

# Заглушка до лучших времен
if __name__ == '__main__':
   print('zaglushko')