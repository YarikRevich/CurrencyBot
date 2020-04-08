import telebot
from telebot import types
import ddd
import sqlite3
import datetime
from datetime import datetime
import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient("localhost",27018)
db = client["parcer"]
collection = db["pars"]

#Передча токену 

bot = telebot.TeleBot("1025174895:AAGI2gUlOasKoFyyueQJtUpovuma7RQbSzs")

#Утворення меседж хендлеру на команду "start"

@bot.message_handler(commands=["start"])

#Утворення клавіатури

def curr(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    stuff1 = types.KeyboardButton("💰Отримати курс доллару")
    stuff2 = types.KeyboardButton("❓Інформація")

    markup.add(stuff1,stuff2)

    #Надсилання привітального повідомлення

    bot.send_message(message.chat.id,"✅Для того,щоб отримати курс на сьогодняшній день натисніть відповідну кнопку",reply_markup=markup)

#Утворення меседж хендлеру на повідомлення типу "text"

@bot.message_handler(content_types=["text"])

#Реакція на повідомлення "💰Отримати курс доллару"

def currency(message):
    if message.text == ("💰Отримати курс доллару"):
        ddd.final()

        data = []


        #Виборка елементів з бд

        pis = collection.find({"_id":1})
        pis1 = collection.find({"_id":2})
        pis2 = collection.find({"_id":3})

        for a in pis:
            data.append(a["curr"])
            
        
            for b in pis1:
                data.append(b["changes"])
        
                for c in pis2:
                    data.append(c["date"])

                    #Надсилання повідомлення з курсом

                    bot.send_message(message.chat.id,"       " + "👇Вся інформація про курс на сьогодні👇"+ "\n" + "На" + " " + data[2] + " " + "💵курс" + " " + "-" + " " + data[0] + "\n" + "📈Що до коливань,то у порівнянні зі вчорашнім днем він збільшився(зменшився) на" + " " + data[1] + " " + "гривень")
        
        
        
     

    #Реакція на повідомлення ""❓Інформація""

    if message.text == ("❓Інформація"):
        bot.send_message(message.chat.id,"❗️Цей бот був спеціально створений на замовлення Дмитра Чернецького)")   
        

bot.polling(none_stop=True)