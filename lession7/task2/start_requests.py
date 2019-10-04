# Вариант "Думаем головой"
import requests

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.71"}


params = {"x-requested-with" : "XMLHttpRequest",
          "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}

page = requests.post('https://www.mvideo.ru/browse/product/gallery-product-list.jsp?galleryId=block5260655&pageType=application&prodId=Site_1&startFrom=5&ref=true&requestId=', headers=headers, params=params)

result = page.url
print('--------')
print(page.text)