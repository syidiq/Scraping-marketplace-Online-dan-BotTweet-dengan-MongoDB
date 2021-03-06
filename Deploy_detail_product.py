import datetime            # Imports datetime library
from datetime import date
import pymongo
from pymongo import MongoClient
import requests
import json
import pandas as pd
import re
import os


def scrap_detail_product(client):
    # Masuk Ke database dan collection
    db =  client["Data_Shopee"]
    collection = db["Data_List_Products"]

    # tetsing koneksi
    collection.count_documents({})
    data_list_product = list(collection.find())
    print(len(data_list_product))
    print(data_list_product[0]['item_basic']['itemid'])
    print(data_list_product[0]['item_basic']['shopid'])


    #Scraping Detal Setiap Product

    data_detail = []
    n = len(data_list_product)

    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
    datetrac = Previous_Date.strftime("%d/%m/%Y")

    cookie = os.getenv("COOKIE")
    for x in range(n):
      headers = {
          'x-api-source': 'pc',
          'cookie': cookie,
          'referer':'https://shopee.co.id/Perawatan-Kecantikan-cat.11043145?page=0&ratingFilter=4',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

      #Indikasi Variabel Scrapping
      itemid = data_list_product[x]['item_basic']['itemid']
      shopid = data_list_product[x]['item_basic']['shopid']
      image = data_list_product[x]['item_basic']['image']
      name = data_list_product[x]['item_basic']['name']
      #print(data_list_product[x]['item_basic']['name'])
      name = re.sub("['/%']", "" , name)
      name = re.sub(' +', ' ', name)
      name = name.replace(' ','-')
      url_img = ('https://cf.shopee.co.id/file/{}').format(image)
      url_prod = ('https://shopee.co.id/-{}-i.{}.{}?sp_atk=bed94b31-50e1-4dc4-a679-13e382568c94&xptdk=bed94b31-50e1-4dc4-a679-13e382568c94').format(name, shopid, itemid)

      #Scraping dan inmput data ke list
      url =("https://shopee.co.id/api/v4/item/get?itemid={}&shopid={}").format(itemid, shopid)
      y = requests.get(url, headers=headers).json()
      y = [y['data']]
      if y[0] != None:
        y[0]['date_transaction'] = datetrac
        y[0]['url_img'] = url_img
        y[0]['url_prod'] = url_prod
        y[0]['harga'] = y[0]['price']/100000
        data_detail.extend(y)

    len(data_detail)


    # Membuat Daily Item Sold 
    db_on = client.get_database('Data_Shopee')
    collection_new = db_on["Data_Products_Detail"]
    
    D_Previous_Date = datetime.datetime.today() - datetime.timedelta(days=2)
    Ddatetrac = D_Previous_Date.strftime("%d/%m/%Y")
    Ddatetrac

    dt_md = list(collection_new.find({'date_transaction': Ddatetrac},{'itemid','shopid','date_transaction','historical_sold'}))
    data_on_daily = []
    if len(dt_md) != 0:
      for i in data_detail:
        df_data_scr = pd.DataFrame([i])[['itemid','shopid','date_transaction','historical_sold']]
        df_dt_md = pd.DataFrame(dt_md)
        result = pd.merge(df_data_scr, df_dt_md, on=["itemid", "shopid"])
        
        if  len(result)!=0:
          aa = result.historical_sold_x
          bb = result.historical_sold_y
          daily_sold_item = aa.tolist()[0] - bb.tolist()[0]
          i['daily_sold_item'] = daily_sold_item
        else:
          i['daily_sold_item'] = 0
        data_on_daily.extend([i])
    else:
      for i in data_detail:
        i['daily_sold_item'] = 0
        data_on_daily.extend([i])
    len(data_on_daily)

    
    collection_new.insert_many(data_on_daily)
