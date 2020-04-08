import bs4,requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient("localhost",27018)
db = client["parcer"]
collection = db["pars"]




#Утворення констант для requests

URL = "https://minfin.com.ua/company/ukrsibbank/currency/"

HEADERS = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36"}

data = []

#Передача url адресси до request

def get_html(url,params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

#Отримання данних про коливання курсу

def get_content(html):
    soup = BeautifulSoup(html.text,"html.parser")
    items = soup.find_all("tbody")       
    r = requests.get("https://minfin.com.ua/company/ukrsibbank/currency/")
    html = bs4.BeautifulSoup(r.text,"html.parser")
    changes = html.select("span.per")
    changes1 = changes[0].get_text().replace("\n", "").replace("+", "")
    data.append(changes1)
    

#Отримання курсу та дати

def jsonparcer():
    r = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/dollar_info?json")
    curss1 = str(r.json()[0]['rate'])
    data.append(curss1)
    curs_data1 = str(r.json()[0]['exchangedate'])
    data.append(curs_data1)
   

#Передача усіх функцій обробнику

def parce():
    html = get_html(URL)
    
    if html.status_code == 200:
        get_content(html)
        jsonparcer()
    else:
        print("Error")


#Утворення бд,таблиці та схем

def final():
    parce()
   
    collection.drop()
    a1 = data[0]
    a2 = data[1]
    a3 = data[2]

    poss = {"_id":1,"curr":a2}
    poss1 = {"_id":2,"changes":a1}
    poss2 = {"_id":3,"date":a3}
    
    
    collection.insert_many([poss,poss1,poss2])




final()
