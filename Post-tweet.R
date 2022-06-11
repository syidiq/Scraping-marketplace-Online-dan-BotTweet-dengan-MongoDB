
library(mongolite)
library(png)
library(grid)
library("jpeg")
library(tidyverse)
library(lubridate)
library(ggplot2)

# Conection Data
username = "syidiq"
password = "syidiq123"
cluster = "clustersyidiq"
code = "3rst0"

connection_string = sprintf('mongodb+srv://%s:%s@%s.%s.mongodb.net/?retryWrites=true&w=majority', username, password, cluster, code)

Data_detail_Products = mongo(collection="Data_Products_Detail",
                             db="Data_Shopee",
                             url=connection_string)
Data_detail_Products$count()


# Date Daily
today <- Sys.Date()-1 #Percobaan di edit jadi dua untuk simulasi ajah (normal=1)
trans_day = format(today, format="%d/%m/%Y")
trans_day

# Top 3 Product Daily Sold
filter = sprintf('{"date_transaction" : "%s"}', trans_day)
data_top3 = Data_detail_Products$find(sort = '{"daily_sold_item" : -1}' ,
                                      limit = 3,
                                      fields = '{"_id" : false,
                                "daily_sold_item" : true,
                                "historical_sold" : true,
                                "harga" : true,
                                "itemid" : true, 
                                "shopid" : true,
                                "date_transaction" : true,
                                "name" : true}',
                                      filter)
dt3 = data.frame(data_top3)
dt3

# Ploting Top 3
plotTop3 = ggplot(dt3,
                  aes(x=reorder(harga,daily_sold_item,),
                      y=daily_sold_item))+
  geom_bar(stat="identity",
           color='gray40',
           fill='#FFC300',)+
  geom_text(aes(label = name),
            color = "red",
            fontface="bold",
            vjust = "inward", 
            hjust = 0,
            size = 3,
            na.rm = TRUE,
            inherit.aes = TRUE)+
  coord_flip()+
  labs(x="Harga Product (Rp.)", y="Penjualan Harian (/pc)", title="Top 3 Product Penjualan Harian Tertinggi") +
  theme(plot.title = element_text(color = "limegreen", , size=20, face="bold"))

plotTop3


# Top 1 Product Daily
itemid_1 = dt3$itemid[1]
shopid_1 = dt3$shopid[1]
filter = sprintf('{"date_transaction" : "%s", "itemid" : %s,"shopid" : %s}', trans_day, itemid_1, shopid_1)
data_top1 = Data_detail_Products$find(filter)
data_top1

# Ploting data
img = data_top1$url_img[1]
img
download.file(img,'y.jpg', mode = 'wb')

jj <- readJPEG("y.jpg",native=TRUE)
g <- rasterGrob(jj, interpolate=TRUE)

ab = qplot(1:10, 1:10, geom="blank") +
  annotation_custom(g, xmin=-Inf, xmax=Inf, ymin=-Inf, ymax=Inf)+
  labs(x="",y='', title="Top 1 Product Penjualan Harian Tertinggi")+
  theme(plot.title = element_text(color = "limegreen", , size=20, face="bold"))
ab


# Conection API Twetter

library(rtweet)

API_Key <- 'JpJOayzuYTvhpnWAhuWOlf44V'
API_Key_Secret <- '0ydxQ5M6k05qYfJON3MgqjnDIukX4IEAAXFWrLmhYA7uWNaPgs'
Access_Token <- '1503956935615279106-j6OWD59SS8mxzA1U2mRPoTGYFgZRs2'
Access_Token_Secret <- 'YfYwCbHe0fmZCd8NqcFqrhEFSolDpSFV7gt2a8XvGZbEn'



twitter_token <- rtweet::create_token(
  app = 'msa_v3',
  consumer_key = API_Key,
  consumer_secret = API_Key_Secret,
  access_token = Access_Token,
  access_secret = Access_Token_Secret
)


# Bahan Postingan
setwd(getwd())

# Saving Gambar
file1 <- tempfile( fileext = ".jpeg")
file2 <- tempfile( fileext = ".jpeg")
ggsave(file1, plot = plotTop3, device = "jpeg", dpi = 144, width = 8, height = 8, units = "in" )
ggsave(file2, plot = ab, device = "jpeg", dpi = 144, width = 8, height = 8, units = "in" )

# hastag
hashtag <- c("ManajemenData", "github", "MongoDB", "NoSQL", "bot", "shopee")

# Detai postingan
status_details <- paste0( "#Bot_Top_Penjualan_Harian_shopee","\n",
                          "Category: Perawatan & Kecantikan","\n",
                          data_top1$url_prod[1], "\n",
                          "Penjualan Harian tertinggi ke-1" , "\n",
                          "pada tanggal :" , Sys.Date()-1, "\n",
                          " penjualan sebesar "
                          ,data_top1$daily_sold_item[1] ," Pc", "\n",
                          " harga product : Rp. ", data_top1$harga[1],
                          "\n",
                          "\n",
                          paste0("#",hashtag, collapse=" ")
)

## Posting to Twitter
allmedia = c(file2,file1)
rtweet::post_tweet(
  status = status_details,
  media = allmedia,
  token = twitter_token
)
