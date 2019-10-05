import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options

# Опшионсы
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")

# загрузка драйвера с Опшионсом и без, для проверки
driver = webdriver.Chrome('.\\chromedriver.exe',chrome_options=chrome_options)  # Optional argument, if not specified will search path.
# driver = webdriver.Chrome('.\\chromedriver.exe')
driver.get('https://www.mvideo.ru')


def monga_monga(dictionary):
    client = MongoClient('localhost', 27017)
    mongo_base = client.mvideo
    collection = mongo_base["mvideo"]
    collection.insert_one(dictionary)
    print('записал в монгу')
    return dictionary

# Ювелирно "прибито гвоздями", но работает. Смысл - нажимать на кнопочки ниже, а не большую кнопку "Вправо".
# Поскольку меньше выборку сделать не удалось пришлось рассчитывать тайминги для циклов. Под термином
# "собирает "Хиты продаж"" я понял название лотов, поэтому складываем в базу имя лота
menu = driver.find_elements_by_css_selector("div.gallery-layout div.section div.gallery-layout.sel-hits-block div.gallery-content.accessories-new div.accessories-carousel-holder.carousel.tabletSwipe a[href^='#']")
i = 0
for knopko in menu:
    if i < 8:
        sleep(5)
        knopko.click()
        if i >=3:
            name = driver.find_elements_by_class_name("sel-product-tile-title")
            for imya in name[0:4]:
                dict = {"Name of good" : imya.text}
                monga_monga(dict)
            i += 1
            print(i)
        else:
            i+=1
            print(i)
    else:
        break