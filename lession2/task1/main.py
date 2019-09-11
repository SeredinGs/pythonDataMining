# импорт хх
# импорт супержоб
#
# Профессия = сус.арг(0)
# Страницы = сус.арг(1)
#
# Колл хх(профессия, Страницы)
# Кол супержоб(профессия, Страницы)
#
# ???
#
# Профит

# Подготовка'

import superjob as ssj
import headhunter as hhr


if __name__ == '__main__':
    name_vac = 'инженер'
    list_num = []
    pages = list('1,2,3,4,5')
    num_pages = [pages[x] for x in range(0, len(pages), 2)]
    print(num_pages)
    # params = {"keywords": name_vac}
    # Делаем реквест
    sj = ssj.superjob()
    hh = hhr.headhunter()

    sj.applyparams(name_vac)
    hh.applyparams(name_vac)

    names, linki, mins, maxs, istochniki = hh.form_list_hh(num_pages)
    reporthh = hh.create_dataframe(names, linki, mins, maxs, istochniki)

    '''
    file = open('output.html','w+', encoding='utf-8')
    file.write(result)
    file.close()
    '''

    df_na_export = sj.form_lists(num_pages)

    sj.export_to_excel(df_na_export, reporthh)

    '''
    # Делаем реквест HH
    # Подготовка
    name_vac = 'data'
    pages = list('1,2,3,4,5')
    num_pages = [pages[x] for x in range(0, len(pages), 2)]
    list_num = []
    '''
