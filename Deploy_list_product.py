
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
      headers = {
          'x-api-source': 'pc',
          'cookie':'REC_T_ID=e67c02b5-ae54-11ec-b368-46ac8e8cc9d8; SPC_F=KrJ9Ck0EYC252EWJ3FSH5QFNzjmvng6O; SPC_IA=-1; _gcl_au=1.1.459910866.1654678938; _fbp=fb.2.1654678939550.956784750; _med=refer; __LOCALE__null=ID; _QPWSDCXHZQA=9be12e07-9c49-426e-e0d8-01a11f73956b; csrftoken=q4gYi0NlKGR1ooZaKW0O1Dm1gnBmthWC; _gid=GA1.3.1577893395.1655378567; G_ENABLED_IDPS=google; G_AUTHUSER_H=0; SPC_CLIENTID=S3JKOUNrMEVZQzI1jkqfwanvqrwehsep; cto_bundle=uAYdV19EWUpOZWVHYUkyUHh0d2RBWDJvTWk1RjVRQjZiWTcwbHAyM1NtWXBpTkRON2xFa3glMkJMWlQ5UW01OW83QjlsaGUlMkZzUyUyQiUyQndDY2dCbWd3b0NoU2p6YU03dmQzY1d5VkUzYmVqWVp5ZiUyQklhSiUyQnJWQW42QWljT3licndaTEp0aCUyRmR6RzIyT1l2QzRyUnFkOWhrWDJ2TTBmQSUzRCUzRA; SPC_P_V=qwX8y4bf4//blCJKuyTV8W3IRhAC1Pd+BhySlTBe2T/avuRWd45jVtSJ4O8dSJ0lOWU7b89UNY2HZFy9qIDt0cs48No/sRJDrNWqYyLOVxRI+BFemR8wpK+1MHptAY0KrkkEGZnFYmwjWlPfG6EbA9F2xQUbvMBVo3iXfm3jeVY=; SPC_T_IV="xSUkgiVIkkLb6i8dQDYG+Q=="; SPC_T_ID="Qgi7GzaMQv5XDqEzLbDFstbVSfohts70RKTV+qyZeV4n9vNxvKhbu6Oe88zLuaJFWn4AUoIUJsN0WyPSS+sFoyQ7F6d7TEDpw7oi7QqshAc="; SPC_ST=.WWpMTDJQT3BNRTljTGM4eEwP+9GcFQuwaUs8vMOw077aVbSbJziWWcvlZD2LHYHxMEfTfmbdx0amYMKQOnFePLi8ai8YqICdaTS0YHjumP5OmDAfntNOLz87jWQvA9zd5K+kS4Y2M6Sr6WeRYlI4k47erE+oNxy1MReQ9r1Km1/l/Od/Vigf0e8skpchZJNWXbQtBfLN5XZUgTZ1lB7Y/w==; SPC_SI=8JWpYgAAAABoOXdhVGRSRYpLHQAAAAAAZWs3MGNydXI=; _ga_KK6LLGGZNQ=GS1.1.1655380505.2.0.1655380537.0; SPC_U=616200160; _ga_SW6D8G0HXK=GS1.1.1655378566.7.1.1655380538.27; _ga=GA1.3.1352849021.1654678939; SPC_R_T_ID=GBKRXT5aeQ+C8w4WBAMvwmEwfEpPfwSQeC7m+DwDAPphEmQBcGXqwRpKvQxUeg5FCQqJCDsoy+5B2yaZI45ZXXk2p4RyRH8RnSPl1P/hw5mPrCxR7tClQ0zwJi+J4nt0ogKbrzn29z5lBoDrMuxYRmYRWgmiFNmUWPvgB15Ke9M=; SPC_R_T_IV=VVBnd2lSMzg4MXp6M3E2SQ==; SPC_T_ID=GBKRXT5aeQ+C8w4WBAMvwmEwfEpPfwSQeC7m+DwDAPphEmQBcGXqwRpKvQxUeg5FCQqJCDsoy+5B2yaZI45ZXXk2p4RyRH8RnSPl1P/hw5mPrCxR7tClQ0zwJi+J4nt0ogKbrzn29z5lBoDrMuxYRmYRWgmiFNmUWPvgB15Ke9M=; SPC_T_IV=VVBnd2lSMzg4MXp6M3E2SQ==; shopee_webUnique_ccd=%2Fa5QJ%2BUJIHhrsvEP3dWqFA%3D%3D%7CvtLwYm6%2BLNOFTz2QB2%2FmN56e0klCIA9tBRtiBblNvRq%2BI2XCScmgQpNMEYn%2Bbntl1EYXBLwfZ0mKX5oMDmF5mwePRg%3D%3D%7CX5Bhx5s%2FskIhcQXV%7C05%7C3; SPC_EC=ZzdUSXRwWHhtb1JjenV6Qju4IY1nhkw2TBr3qFHlMxwaA+/I6aP0ZgK1JxwGJ4aUWZa4NJH2iC2980GS4UPibq/oNFWuJRv1B9TPQTpLf6mdJOIrH+wgvc8xvMpg567jHSMopi3m4gVH0HprqCHau1I3b+LWa85oDmayECbuhCs=',
          'referer':'https://shopee.co.id/Perawatan-Kecantikan-cat.11043145?page=0&ratingFilter=4',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}
      
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
