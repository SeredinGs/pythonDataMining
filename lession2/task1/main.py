# основной модуль. в нём задаются имя професии и номра страниц
import superjob as ssj
import headhunter as hhr
import sys


if __name__ == '__main__':
    name_vac = sys.argv[1]
    list_num = []
    pages = list(sys.argv[2])
    num_pages = [pages[x] for x in range(0, len(pages), 2)]
    print('Ищу вакансии для профессии {}, по страницам {}'.format(name_vac, num_pages))

    # params = {"keywords": name_vac}
    # Делаем реквест
    sj = ssj.superjob()
    hh = hhr.headhunter()

    sj.applyparams(name_vac)
    hh.applyparams(name_vac)

    reporthh = hh.form_list_hh(num_pages)
    df_na_export = sj.form_lists(num_pages)

    sj.export_to_excel(df_na_export, reporthh)