import requests

headers = {"adrum_0": "g:d3842ca6-ddd1-4b9f-a012-42dde53e31fd",
            "adrum_1": "n:customer1_b8e1f0e6-cc5b-4da4-a095-00a44385df2e",
            "adrum_2": "i:2695",
            "adrum_3": "e:57"}
a = requests.get('https://www.mvideo.ru/browse/product/gallery-product-list.jsp?galleryId=block5260655&pageType=application&prodId=Site_1&startFrom=5&ref=true&requestId=', headers=headers)
requests.content