# основной модуль. в нём задаются имя професии и номра страниц
import superjob as ssj
import headhunter as hhr
import sys

# для того, чтобы запустить поиск максимальной зп нужно добавить параметр "макс" см. readme
if __name__ == '__main__':
    name_vac = sys.argv[1]
    list_num = []
    if sys.argv[1] != 'макс':
        count_pages = sys.argv[2]
        num_pages = [x for x in range(0, int(count_pages) + 1)]
        print('Ищу вакансии для профессии {}, по страницам {}'.format(name_vac, num_pages))

        # params = {"keywords": name_vac}
        # Делаем реквест
        sj = ssj.superjob()
        hh = hhr.headhunter()

        sj.applyparams(name_vac)
        hh.applyparams(name_vac)

        names, linki, mins, maxs, istochniki = hh.form_list_hh_monga(num_pages)
        hh.inserttomonga(name_vac, names, linki, mins, maxs, istochniki)
        names, linki, mins, maxs, istochniki = sj.form_lists_monga(num_pages)
        sj.inserttomonga(name_vac, names, linki, mins, maxs, istochniki)
    else:
        sj = ssj.superjob()
        name_vac = sys.argv[2]
        zp = sys.argv[3]
        sj.get_max(name_vac, zp)
