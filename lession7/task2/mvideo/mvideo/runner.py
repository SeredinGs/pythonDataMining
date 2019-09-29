from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# HH неплохо прошел прогон на конфиге от SJ, поэтому я оставил всё как есть
from mvideo import settings
from mvideo.spiders.pauchok import PauchokSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(PauchokSpider)
    process.start()
