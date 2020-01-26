# -*- coding:utf-8 -*-
from pymongo import MongoClient

client = MongoClient('192.168.1.8', 27017)

db = client['stocks']
