
# Panggil Library
import datetime          
from datetime import date
import pymongo
from pymongo import MongoClient
import requests
import json
import pandas as pd
import re
import os

# Iport Deploy
import Deploy_detail_product
import Deploy_list_product

# Coneksi ke data MongoDB
username = os.getenv(USERNAME_MONGODB)
password = os.getenv(PASSWORD_MONGODB)
cluster = os.getenv(CLUSTER_MONGODB)
code = os.getenv(CODE_MONGODB)
uri = ("mongodb+srv://{}:{}@{}.{}.mongodb.net/?retryWrites=true&w=majority").format(username,password,cluster,code)
# start client to connect to MongoDB server 
client = MongoClient(uri)

# Menjalankan Deploy
Deploy_list_product.scrap_list_product(client)
Deploy_detail_product.scrap_detail_product(client)

