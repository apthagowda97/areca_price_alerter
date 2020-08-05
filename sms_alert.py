import pandas as pd
import requests
import configparser
from twilio.rest import Client
from bs4 import BeautifulSoup


def read_config(filename):
    """Reads the config file."""
    
    config = configparser.ConfigParser()
    config.read(filename)

    return config

def parse_url(url:str):
    """Parses the URL and returns the Areca Price data as DataFrame"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price_table = soup.find(id="_ctl0_content5_Table1")
    price_df = pd.read_html(str(price_table),header=0)[0]

    return price_df

def get_message_body(price_df,city:str):
    """" Returns message body consisting of Areca price for the given city"""

    if city in price_df.Market.values:
        data = price_df[price_df['Market']==city][['Variety','Market Date','Maximum Price']].sort_values('Variety').values.tolist()
        body = f'\n  {city}\n'
        for row in data:
            body += '{0}({1}): {2}\n'.format(row[0][:5],row[1].split('/')[0],row[2])
        return body
    else:
        return None

def send_sms(body:str,config):
    """Send the SMS with given message body."""

    account_sid =  config['twilio']['account_sid']
    auth_token  =  config['twilio']['auth_token']
    from_phone  =  config['twilio']['from_phone']
    to_phone    =  config['twilio']['to_phone']

    client = Client(account_sid, auth_token) 
    client.messages.create(from_=from_phone,body=body,to=to_phone)

if __name__=='__main__':

    config = read_config('config.ini')
    price_df = parse_url(open('url.txt').read())
    body = get_message_body(price_df,'SHIVAMOGGA')
    send_sms(body,config)