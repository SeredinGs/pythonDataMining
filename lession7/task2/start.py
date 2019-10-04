# ЗАДАНИЕ
# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint


driver = webdriver.Firefox(executable_path='.\\geckodriver.exe')

driver.get('https://www.mvideo.ru')

menu = driver.find_elements_by_css_selector("div.gallery-layout div.section div.gallery-layout.sel-hits-block div.gallery-content.accessories-new div.accessories-carousel-holder.carousel.tabletSwipe a[href^='#']")

i = 0

for knopko in menu:
    if i < 7:
        sleep(3)
        knopko.click()
        if i >=2:
            print('parse blocks')
            i += 1
            print(i)
        else:
            i+=1
            print(i)
    else:
        break
