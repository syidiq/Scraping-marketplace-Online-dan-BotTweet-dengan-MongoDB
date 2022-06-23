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
          'cookie':'REC_T_ID=e67c02b5-ae54-11ec-b368-46ac8e8cc9d8; SPC_F=KrJ9Ck0EYC252EWJ3FSH5QFNzjmvng6O; SPC_IA=-1; _gcl_au=1.1.459910866.1654678938; _fbp=fb.2.1654678939550.956784750; _med=refer; G_ENABLED_IDPS=google; SPC_CLIENTID=S3JKOUNrMEVZQzI1jkqfwanvqrwehsep; cto_bundle=uAYdV19EWUpOZWVHYUkyUHh0d2RBWDJvTWk1RjVRQjZiWTcwbHAyM1NtWXBpTkRON2xFa3glMkJMWlQ5UW01OW83QjlsaGUlMkZzUyUyQiUyQndDY2dCbWd3b0NoU2p6YU03dmQzY1d5VkUzYmVqWVp5ZiUyQklhSiUyQnJWQW42QWljT3licndaTEp0aCUyRmR6RzIyT1l2QzRyUnFkOWhrWDJ2TTBmQSUzRCUzRA; SPC_T_IV="xSUkgiVIkkLb6i8dQDYG+Q=="; SPC_T_ID="Qgi7GzaMQv5XDqEzLbDFstbVSfohts70RKTV+qyZeV4n9vNxvKhbu6Oe88zLuaJFWn4AUoIUJsN0WyPSS+sFoyQ7F6d7TEDpw7oi7QqshAc="; SPC_ST=.WWpMTDJQT3BNRTljTGM4eEwP+9GcFQuwaUs8vMOw077aVbSbJziWWcvlZD2LHYHxMEfTfmbdx0amYMKQOnFePLi8ai8YqICdaTS0YHjumP5OmDAfntNOLz87jWQvA9zd5K+kS4Y2M6Sr6WeRYlI4k47erE+oNxy1MReQ9r1Km1/l/Od/Vigf0e8skpchZJNWXbQtBfLN5XZUgTZ1lB7Y/w==; _ga_KK6LLGGZNQ=GS1.1.1655380505.2.0.1655380537.0; SPC_U=616200160; SPC_R_T_ID=GBKRXT5aeQ+C8w4WBAMvwmEwfEpPfwSQeC7m+DwDAPphEmQBcGXqwRpKvQxUeg5FCQqJCDsoy+5B2yaZI45ZXXk2p4RyRH8RnSPl1P/hw5mPrCxR7tClQ0zwJi+J4nt0ogKbrzn29z5lBoDrMuxYRmYRWgmiFNmUWPvgB15Ke9M=; SPC_R_T_IV=VVBnd2lSMzg4MXp6M3E2SQ==; SPC_T_ID=GBKRXT5aeQ+C8w4WBAMvwmEwfEpPfwSQeC7m+DwDAPphEmQBcGXqwRpKvQxUeg5FCQqJCDsoy+5B2yaZI45ZXXk2p4RyRH8RnSPl1P/hw5mPrCxR7tClQ0zwJi+J4nt0ogKbrzn29z5lBoDrMuxYRmYRWgmiFNmUWPvgB15Ke9M=; SPC_T_IV=VVBnd2lSMzg4MXp6M3E2SQ==; __LOCALE__null=ID; SPC_SI=it+yYgAAAABpWlFkVlB5QlEqDgAAAAAAeThJaEw1TTE=; _QPWSDCXHZQA=9be12e07-9c49-426e-e0d8-01a11f73956b; csrftoken=jtEMwkdpNnpWeb8z2kpJeTIeWo5igaYC; _ga_SW6D8G0HXK=GS1.1.1655971115.10.0.1655971115.60; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.3.1352849021.1654678939; _gid=GA1.3.250130070.1655971116; _dc_gtm_UA-61904553-8=1; shopee_webUnique_ccd=O%2Byy5VcAsFNARtMtsrj7MA%3D%3D%7CPhGHIQ5NiaHvxcj1yf%2Bg0S1pNBKbLzW6E%2BGU7KUCilO5s1b0ddjRYjTkYfz85%2FFdJNMWT7xWaSAQ3FLQllPySvA%3D%7CGbB4CCOf6ZFpwssB%7C05%7C3; SPC_EC=aHBITW82Ykdmb3AwYkhOM8XIGH4JSCUp5KK+818qEbqcyJoGmiAFVyixmNPWyQgF+itqkycWZSbHpk6PaJ/zJeLoPYVxptLvAaSbYe1KaGZ996X7QqwiBZjcu0jwUfvdOc9gvN06xG65ScrDDNbQF8E4p6l9EtXAl/0AIzgguB4=',
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
