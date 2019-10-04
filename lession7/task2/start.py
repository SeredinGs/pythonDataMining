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

# knopochki = driver.find_elements_by_xpath('//div[@class="gallery-layout"]/div[@class="section"]/div[@class="gallery-layout sel-hits-block"]/*/div[@class="carousel-paging"]')
#knopochki = driver.find_elements_by_xpath('//div[@class="carousel-paging"]/a')
'''
knopochki = driver.find_elements_by_css_selector('div.gallery-layout div.section div.gallery-layout.sel-hits-block div.gallery-content.accessories-new div.accessories-carousel-holder.carousel.tabletSwipe div.carousel-paging a')
print('d')

for knopko in knopochki:
    knopko.click()
   '''
menu = driver.find_element_by_css_selector("div.gallery-layout div.section div.gallery-layout.sel-hits-block div.gallery-content.accessories-new")
#sleep(5)
hidden_submenu = driver.find_element_by_css_selector("a.next-btn.sel-hits-button-next")

driver.execute_script("window.scrollTo(0, 894);")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.perform()
sleep(5)
actions.click(hidden_submenu)
actions.click(hidden_submenu)
actions.click(hidden_submenu)
sleep(2)
actions.perform()
