import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

driver = webdriver.Chrome('.\\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://www.mvideo.ru')

menu = driver.find_element_by_css_selector("div.gallery-layout div.section div.gallery-layout.sel-hits-block div.gallery-content.accessories-new")
#sleep(5)
hidden_submenu = driver.find_element_by_css_selector("a.next-btn.sel-hits-button-next")

driver.execute_script("window.scrollTo(0, 894);")
actions = ActionChains(driver)
actions.move_to_element(menu)
actions.perform()
sleep(2)
actions.click(hidden_submenu)
actions.click(hidden_submenu)
actions.click(hidden_submenu)
sleep(2)
actions.perform()