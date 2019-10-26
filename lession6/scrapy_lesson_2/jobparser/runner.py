import os
from os.path import join, dirname
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.instagram import InstagramSpider

do_env = join(dirname(__file__), '.env') # из venv метод не читается, пришлось .env перенести в корень
load_dotenv(do_env)

#Загружаем переменные из окружения
INST_LOGIN = os.getenv('INST_LOGIN')
INST_PSWRD = os.getenv('INST_PSWRD')

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
   # process.crawl(HhruSpider)

    #Передаем параметры при запуске паука
    process.crawl(InstagramSpider,['geekbrains','python'],INST_LOGIN,INST_PSWRD)
    process.start()
