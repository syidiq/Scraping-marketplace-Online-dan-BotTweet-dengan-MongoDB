

def scrap_list_product(client):
    
    # Scraping List Product
    data = []
    for x in range(50):

      #ua = UserAgent()
      #ua.chrome
      headers = {
          'x-api-source': 'pc',
          'cookie':'csrftoken=XluKetIaszJef9Dhqd4vH2SJkg8j08NM; SPC_F=ehzz4u9d8wEJj5rUqz6LgfzW9s50nwWe; REC_T_ID=3df12030-992b-11ec-b282-a687c864b5ca; _fbp=fb.2.1646117154675.322222415; _QPWSDCXHZQA=eb581e14-b8eb-496f-e327-4a382e55343f; __LOCALE__null=ID; G_ENABLED_IDPS=google; G_AUTHUSER_H=0; SPC_CLIENTID=ZWh6ejR1OWQ4d0VKqaanfcaidpxshjpb; SPC_IA=1; _med=affiliates; SPC_U=-; SPC_EC=-; _gcl_au=1.1.2006356178.1653963194; SPC_SI=mall.tJkYe12AWb7sZHR0e32iZ4XuuxAlZzJK; _gid=GA1.3.1659451253.1654590537; SPC_T_IV="oOM7YjH2HBIobxkTA1gKHA=="; SPC_T_ID="TPjee1XbDY4RSMzCqH9S5UmbEHFIVAmM0wW0YZHV2v2pC2Km6NukSg8+CvaLyo8yKzIuT9e92j2urVgTVWf3/hC7q0j1KsdoKklCoCE/gmQ="; SPC_R_T_IV=yZzoYuK8yZ6MuMzCnydn5w==; SPC_T_ID=KoeskXzGd8CEzcxhvSdLLzA8aCozGo8GciGqtmw3N8xOfUczXie1QBy1qj3gOBkcNINcERcnzsmODFamkJOuqmP2cay4HbndH/SP4IdhYPM=; SPC_T_IV=yZzoYuK8yZ6MuMzCnydn5w==; SPC_R_T_ID=KoeskXzGd8CEzcxhvSdLLzA8aCozGo8GciGqtmw3N8xOfUczXie1QBy1qj3gOBkcNINcERcnzsmODFamkJOuqmP2cay4HbndH/SP4IdhYPM=; cto_bundle=PiBiWV9mNzNHZjVDYXVTTjhqYWJQY3h1SW1aSmZGeEoyU01xVkNMQXJ1cTNKYSUyQiUyQkFnJTJCUEd0aFk0WHE3MDZaSWNLSHNybk13Nmw0QjZHVkhTeGxuNmVDQUxkeFRMY3BmZVk0RUl0TmNOanphNE9nTTdJMjJvazYlMkI1ZmlwZjdpelVOVjk1S1BHdEFnRjF6UUpyMU5la3N0Sm4lMkJBJTNEJTNE; _ga=GA1.3.240409233.1646117158; _ga_SW6D8G0HXK=GS1.1.1654679373.14.0.1654679373.60; shopee_webUnique_ccd=u46yCpH31P8TtfX6p7QM%2BA%3D%3D%7C3qdZ7aGegp2kzOdgzD%2BHqr8SCmPEgSAvX%2Bjxh3zXrkH1dWEFuWZKVlYIl5SngOKMGyabOuttaV2P1pwsWYQ2gtoNcxM%3D%7C3vImPC4JcsQcVKhb%7C05%7C3',
          'referer':'https://shopee.co.id/Perawatan-Kecantikan-cat.11043145?page=0&ratingFilter=4',
          'User-Agent': Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36}
      
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
    
    db_new = client["Data_Shopee"]
    collection_new = db_new["Data_List_Products"]
    collection_new.insert_many(data_new)
