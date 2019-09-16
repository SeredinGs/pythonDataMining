from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
import pandas as pd
import datetime

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.testmongi
col = db['_testovaya']


# print(type(new_posts))
# # raise Exception


list1 = ['a','b','v','g','d']
list2 = ['http://doiki.com',"http://nedoiki.com",'','http://banzaka.com','http://joycasino1.com']
list3 = ['8','Не указано','56','','67']
list4 = ['2',3,'','8','1']

dic = {"name":None, "linka":None, "min":None, "max":None}
total_list = list()
for l1,l2,l3,l4 in zip(list1,list2,list3,list4):
    dic["name"] = l1
    dic["linka"] = l2
    if l3 == 'Не указано' or l3 == '':
        l3 = 0
        dic["min"] = int(l3)
    else:
        dic["min"] = int(l3)
    if l4 == '':
        l4 = 0
        dic["max"] = int(l4)
    else:
        dic["max"] = int(l4)
    #print(dic)
    total_list.append(dic.copy())
print(total_list)

col.insert_many(total_list)

