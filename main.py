import os
import telebot 
import requests
import telebot
from datetime import date
import json
import time
from threading import Thread
import schedule
from telebot.util import ThreadPool

keepRunning=False
APIKEY="1707199286:AAFaaMbgHHTM9B4f_01ejOqfvvDsRgkBYs0"
PINCODE="390019"
bot = telebot.TeleBot(APIKEY)
print(bot.get_chat_member)
today = date.today()
d1 = today.strftime("%d-%m-%Y")
PINCODE_URL="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
PINCODE_HEADERS={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
PINCODE_PARAMS={"pincode":PINCODE,"date":d1}
chatRecords={"default":""}

# Initiate the chat 
@bot.message_handler(commands=['help'])
def send_welcome(message):
    chatRecords['default']=message.chat.id
    bot.send_message(message.chat.id, "use /begin and then Send me a message in following format to register your PINCODE -> PINCODE <PINCODE>")

# Initiate the chat 
@bot.message_handler(commands=['begin'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Enter your email Address in following format EMAIL <email>")

#Register the chat 
@bot.message_handler(regexp="*EMAIL{1} ")
def handle_message(message):
    temp_email=message.text[7:]
    print("You have entered the following PINCODE : "+message.text[-6:])

  
# Ask for the PINCODE 
@bot.message_handler(regexp="*PASSCODE{1} \d{6}")
def handle_message(message):
    PINCODE=message.text[-6:]
    print("You have entered the following PINCODE : "+message.text[-6:])
    

# define the loop start 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keepRunning=True
    bot.send_message(message.chat.id, " The Alert system has been Activated")

# define the loop start 
@bot.message_handler(commands=['stop'])
def send_welcome(message):
    keepRunning=False
    bot.send_message(message.chat.id, " The Alert system has been Deactivated")


def sendReq():
    response=requests.get(PINCODE_URL,headers=PINCODE_HEADERS,params=PINCODE_PARAMS)
    responseJson=json.loads(response.text)
    Sessions=responseJson['sessions']
    for center in Sessions:
        if(center['available_capacity_dose1']>0 and center['min_age_limit']==18):
            print(center['name'] + " Has Slots available for 18+")
            bot.send_message(chatRecords['default'],center['name']+" Has slots available -> "+center['available_capacity_dose1'])

schedule.every(15).minutes.do(sendReq)

while (True):
    schedule.do_pending()
    time.sleep(1000)
#Thread(target = alerts).start()
