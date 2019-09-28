from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# HH неплохо прошел прогон на конфиге от SJ, поэтому я оставил всё как есть
from jobparser import settings_SJ
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sj import SjSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings_SJ)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjSpider)
    process.start()
