import os
import telebot 
import requests
from datetime import date
import json


today = date.today()
d1 = today.strftime("%d-%m-%Y")

url_generate_otp="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
headers_generate_otp={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

payload_pin={"pincode":"390019","date":"23-05-2021"}
response=requests.get(url_generate_otp,headers=headers_generate_otp,params=payload_pin)
responseJson=json.loads(response.text)
Sessions=responseJson['sessions']

for center in Sessions:
  if(center['available_capacity_dose1']>0 and center['min_age_limit']==18):
    print(center['name'] + " Has Slots available for 18+")

