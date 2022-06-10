
# Panggil Library
import datetime          
from datetime import date
import pymongo
from pymongo import MongoClient
import requests
import json
import pandas as pd
import re

# Iport Deploy
import Deploy_detail_product
import Deploy_list_product

# Coneksi ke data MongoDB
username = "syidiq"
password = "syidiq123"
cluster = "clustersyidiq"
code = "3rst0"
uri = ("mongodb+srv://{}:{}@{}.{}.mongodb.net/?retryWrites=true&w=majority").format(username,password,cluster,code)
# start client to connect to MongoDB server 
client = MongoClient(uri)

# Menjalankan Deploy
Deploy_list_product.scrap_list_product(client)
Deploy_detail_product.scrap_detail_product(client)

