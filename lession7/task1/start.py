# ЗАДАНИЕ
# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
# о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

# функция монги была позаимствована из дз про скрапи
def monga_monga(dictionary):
    client = MongoClient('localhost', 27017)
    mongo_base = client.selenium_mail_ru
    collection = mongo_base["mail_ru"]
    collection.insert_one(dictionary)
    print('записал в монгу')
    return dictionary


driver = webdriver.Firefox(executable_path='.\\geckodriver.exe')

driver.get('http://www.mail.ru')

textbox_login = driver.find_element_by_id("mailbox:login")
textbox_login.send_keys('study.ai_172@mail.ru')

baton_type_paswd = driver.find_element_by_id("mailbox:submit")
baton_type_paswd.click()

# Поскольку элемент скрыт для него не получится использовать expected_conditions. Пользуемся слипом
sleep(5)

textbox_paswd = driver.find_element_by_id("mailbox:password")
textbox_paswd.send_keys('Password172')
textbox_paswd.send_keys(Keys.RETURN)

#sleep(5)
strochka = WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'llc__container'))
        )
# считаем сколько у нас писем
count = len(driver.find_elements_by_class_name('llc__container'))

# обнуляем итератор
i=0

# решение задачи: будем проходить по ссылкам на письма, читать всё и возвращаться обратно
# смысл итератора в том, что после перехода из страницы письма во "Входящие" страница некорректно отображалась, поэтому
# делался принудительный рефреш и повторно проводилось чтение списка писем и согласно итератора переходили на нужную
# ссылку

for i in range(0, count):
    driver.refresh()

    # ждем, пока мсье драйвер покажет страницу
    stroka = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'llc__container'))
    )
    stroka = driver.find_elements_by_class_name('llc__container')
    # указываем ему номер
    letter = stroka[i]
    letter.click()

    # забираем всё, что нам нужно
    name = driver.find_element_by_class_name('letter__contact-item').text
    datetime = driver.find_element_by_class_name('letter__date').text
    content = driver.find_element_by_class_name('letter__body').text
    # примитивный вывод
    print(f'{name}, {datetime}, {content}')
    # пишем в монгу
    dict = {"sender": name, "date": datetime, "body": content}
    monga_monga(dict)
    driver.back()