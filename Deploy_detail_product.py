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


    for x in range(n):
      headers = {
          'x-api-source': 'pc',
          'cookie':'csrftoken=XluKetIaszJef9Dhqd4vH2SJkg8j08NM; SPC_F=ehzz4u9d8wEJj5rUqz6LgfzW9s50nwWe; REC_T_ID=3df12030-992b-11ec-b282-a687c864b5ca; _fbp=fb.2.1646117154675.322222415; _QPWSDCXHZQA=eb581e14-b8eb-496f-e327-4a382e55343f; __LOCALE__null=ID; G_ENABLED_IDPS=google; G_AUTHUSER_H=0; SPC_CLIENTID=ZWh6ejR1OWQ4d0VKqaanfcaidpxshjpb; SPC_IA=1; _med=affiliates; SPC_U=-; SPC_EC=-; _gcl_au=1.1.2006356178.1653963194; SPC_SI=mall.tJkYe12AWb7sZHR0e32iZ4XuuxAlZzJK; _gid=GA1.3.1659451253.1654590537; SPC_T_IV="oOM7YjH2HBIobxkTA1gKHA=="; SPC_T_ID="TPjee1XbDY4RSMzCqH9S5UmbEHFIVAmM0wW0YZHV2v2pC2Km6NukSg8+CvaLyo8yKzIuT9e92j2urVgTVWf3/hC7q0j1KsdoKklCoCE/gmQ="; SPC_R_T_IV=yZzoYuK8yZ6MuMzCnydn5w==; SPC_T_ID=KoeskXzGd8CEzcxhvSdLLzA8aCozGo8GciGqtmw3N8xOfUczXie1QBy1qj3gOBkcNINcERcnzsmODFamkJOuqmP2cay4HbndH/SP4IdhYPM=; SPC_T_IV=yZzoYuK8yZ6MuMzCnydn5w==; SPC_R_T_ID=KoeskXzGd8CEzcxhvSdLLzA8aCozGo8GciGqtmw3N8xOfUczXie1QBy1qj3gOBkcNINcERcnzsmODFamkJOuqmP2cay4HbndH/SP4IdhYPM=; cto_bundle=PiBiWV9mNzNHZjVDYXVTTjhqYWJQY3h1SW1aSmZGeEoyU01xVkNMQXJ1cTNKYSUyQiUyQkFnJTJCUEd0aFk0WHE3MDZaSWNLSHNybk13Nmw0QjZHVkhTeGxuNmVDQUxkeFRMY3BmZVk0RUl0TmNOanphNE9nTTdJMjJvazYlMkI1ZmlwZjdpelVOVjk1S1BHdEFnRjF6UUpyMU5la3N0Sm4lMkJBJTNEJTNE; _ga=GA1.3.240409233.1646117158; _ga_SW6D8G0HXK=GS1.1.1654679373.14.0.1654679373.60; shopee_webUnique_ccd=u46yCpH31P8TtfX6p7QM%2BA%3D%3D%7C3qdZ7aGegp2kzOdgzD%2BHqr8SCmPEgSAvX%2Bjxh3zXrkH1dWEFuWZKVlYIl5SngOKMGyabOuttaV2P1pwsWYQ2gtoNcxM%3D%7C3vImPC4JcsQcVKhb%7C05%7C3',
          'referer':'https://shopee.co.id/Perawatan-Kecantikan-cat.11043145?page=0&ratingFilter=4',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}

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

    D_Previous_Date = datetime.datetime.today() - datetime.timedelta(days=2)
    Ddatetrac = D_Previous_Date.strftime("%d/%m/%Y")
    Ddatetrac

    dt_md = list(collection.find({'date_transaction': Ddatetrac},{'itemid','shopid','date_transaction','historical_sold'}))
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



    db_on = client.get_database('Data_Shopee')
    collection_new = db_on["Data_Products_Detail"]
    collection_new.insert_many(data_on_daily)
