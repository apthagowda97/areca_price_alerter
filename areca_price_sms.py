import time
import pandas as pd
import requests
import configparser
import urllib.request
from twilio.rest import Client
from bs4 import BeautifulSoup


config = configparser.ConfigParser()
config.read('config.ini')

account_sid = config['twilio']['account_sid']
auth_token = config['twilio']['auth_token']
from_phone = config['twilio']['from_phone']
to_phone = config['twilio']['to_phone']

client = Client(account_sid, auth_token) 
url = 'https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=140&VarCode=1&Date=12/10/2018&CommName=Arecanut%20/%20%E0%B2%85%E0%B2%A1%E0%B2%BF%E0%B2%95%E0%B3%86&VarName=Red%20/%20%E0%B2%95%E0%B3%86%E0%B2%82%E0%B2%AA%E0%B3%81'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find(id="_ctl0_content5_Table1")

price_df = pd.read_html(str(table),header=0)[0]
cities =  ['SHIVAMOGGA','TIRTHAHALLI']


for city in cities:
    if city in price_df.Market.values:
        data = price_df[price_df['Market']==city][['Variety','Market Date','Maximum Price']].sort_values('Variety').values.tolist()
        message_body = f'\n  {city}\n'
        for row in data:
            message_body += '{0}[{1}]:{2}\n'.format(row[0][:6],row[1].split('/')[0],row[2])
        message = client.messages.create(from_=from_phone,body=message_body,to=to_phone)
        print(message_body)