#web scraping and printing the scraped 
import requests
from bs4 import BeautifulSoup
import pandas
flip_url="https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY"
req=requests.get(flip_url)
content=req.content
soup=BeautifulSoup(content,"html.parser")

all_phone=soup.find_all("div",{"class":"_3O0U0u"})
for phone in all_phone:
    
    phone_name=phone.find("div",{"class":"_3wU53n"}).text
    phone_rate=phone.find("div",{"class":"_6BWGkk"}).text
    print(phone_name, phone_rate)
 
 
  OUTPUT:
  Vivo U10 (Thunder Black, 32 GB) ₹9,990₹10,9909% off
Realme 6 (Comet Blue, 128 GB) ₹16,999
POCO X2 (Atlantis Blue, 128 GB) ₹18,499₹18,9992% off
Realme Narzo 10 (That Green, 128 GB) ₹11,999₹12,9997% off
Vivo Z1Pro (Sonic Black, 64 GB) ₹14,990₹17,99016% off
Vivo Z1Pro (Sonic Black, 128 GB) ₹16,990₹20,99019% off
Vivo Z1Pro (Sonic Black, 64 GB) ₹13,990₹15,99012% off
Vivo U10 (Electric Blue, 64 GB) ₹10,490₹11,99012% off
Vivo Z1Pro (Sonic Blue, 64 GB) ₹13,990₹15,99012% off
Vivo Z1Pro (Sonic Blue, 128 GB) ₹16,990₹20,99019% off
Vivo Z1Pro (Sonic Blue, 64 GB) ₹14,990₹17,99016% off
Vivo Y15 (Burgundy Red, 64 GB) ₹12,990₹15,99018% off
Vivo Y15 (Aqua Blue, 64 GB) ₹12,990₹15,99018% off
Redmi Note 7 Pro (Space Black, 64 GB) ₹12,999₹16,99923% off
Realme Narzo 10 (That White, 128 GB) ₹11,999₹12,9997% off
Realme 5 Pro (Sparkling Blue, 64 GB) ₹13,999₹14,9996% off
Realme 5 Pro (Sparkling Blue, 128 GB) ₹16,999₹17,9995% off
Realme 5 Pro (Sparkling Blue, 64 GB) ₹14,999₹15,9996% off
Redmi Note 8 Pro (Shadow Black, 64 GB) ₹15,999₹16,9995% off
Micromax X380 ₹740₹1,49950% off
Mi A2 (Black, 64 GB) ₹10,599₹17,49939% off
Vivo U10 (Electric Blue, 32 GB) ₹9,990₹10,9909% off
POCO F1 (Steel Blue, 256 GB) ₹17,999₹30,99941% off
Redmi Note 8 Pro (Electric Blue, 128 GB) ₹16,999₹17,9995% off




#CODE FOR DATABASE
#CREATE FILE NAMED CONNECT AND WRITE THE OF DATABASE


import sqlite3
def connect(dbname):
    conn=sqlite3.connect(dbname)
    conn.execute("CREATE TABLE IF NOT EXISTS FLIP_PHONES(NAME,PRICE) ")
    print("table created succesfully!")
    conn.close()
    
def insert_into_table(dbname,values):
    conn=sqlite3.connect(dbname)
    print("Inserted into table:"+str(values))
    insert_sql="INSERT INTO FLIP_PHONES(NAME,PRICE) VALUES (?,?)"
    conn.execute(insert_sql,values )
    conn.commit()
    conn.close()

def get_phone_info(dbname):
    conn=sqlite3.connect(dbname)
    
    cur=conn.cursor()
    cur.execute("SELECT *FROM FLIP_PHONES")
    table_data=cur.fetchall()
    for record in table_data:
        print(record)
    conn.close()
    
  #NOW CREATE AN OTHER FILE
  #IMPORT THE CONNECT FILE IN IT
  
  import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import import_ipynb
import connect

parser = argparse.ArgumentParser()
parser.add_argument("--dbname", help="Enter the name of db", type=str)
args=parser.parse_args()

flip_url="https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
page_num_MAX = 3
scraped_info_list=[]
connect.connect(args.dbname)

for page_num in range(1, page_num_MAX):
    req=requests.get(flip_url+ str(page_num))
    content=req.content
    soup=BeautifulSoup(content,"html.parser")
    all_phone=soup.find_all("div",{"class":"_3O0U0u"})
    
    for phone in all_phone:
        phone_dict={}
        phone_dict["name"]=phone.find("div",{"class":"_3wU53n"}).text
        phone_dict["rate"]=phone.find("div",{"class":"_6BWGkk"}).text
    #print(phone_name, phone_rate)
        scraped_info_list.append(phone_dict)
        connect.insert_into_table(args.dbname,tuple(phone_dict.values()))
                                  
dataframe = pandas.DataFrame(scraped_info_list)
dataframe.to_csv("flip.csv")
connect.get_phone_info(args.dbname)

#THUS THE OUT IS STORED IN DATABASE AND CSV FILE
