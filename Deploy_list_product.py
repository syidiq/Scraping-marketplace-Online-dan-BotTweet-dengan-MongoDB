
import datetime            # Imports datetime library
from datetime import date
import pymongo
from pymongo import MongoClient
import requests
import json
import pandas as pd
import re
import os

def scrap_list_product(client):
    
    # Scraping List Product
    data = []
    for x in range(50):

      #ua = UserAgent()
      #ua.chrome
      cookie = os.getenv("COOKIE")
      headers = {
          'x-api-source': 'pc',
          'cookie': cookie,
          'referer':'https://shopee.co.id/Perawatan-Kecantikan-cat.11043145?page=0&ratingFilter=4',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
      
      number_page = x*60
      url =("https://shopee.co.id/api/v4/search/search_items?by=relevancy&limit=60&match_id=11043145"
            "&newest={}&order=desc&page_type=search&rating_filter=4&scenario=PAGE_OTHERS&version=2").format(number_page)
      y = requests.get(url, headers=headers).json()
      data.extend(y['items'])
    len(data)

    # pemeriksaan List product yang belum ada
    db_new = client["Data_Shopee"]
    collection_new = db_new["Data_List_Products"]
    dt_md = list(collection_new.find({},{'itemid','shopid'}))
    df_dt_md = pd.DataFrame(dt_md)

    data_new = []

    if len(dt_md) != 0:
      for i in data:
        df_data_scr = pd.DataFrame([i])[['itemid','shopid']]
        result = pd.merge(df_data_scr, df_dt_md, on=["itemid", "shopid"])
        if  len(result)==0:
          data_new.extend([i])
    else:
      data_new = data

    len(data_new)
    
    if len(data_new) != 0:
        db_new = client["Data_Shopee"]
        collection_new = db_new["Data_List_Products"]
        collection_new.insert_many(data_new)
