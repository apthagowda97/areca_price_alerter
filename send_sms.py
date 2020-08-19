import configparser
from twilio.rest import Client


def read_config(filename):
    """Reads the config file."""
    
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def send_sms(body:str):
    """Send the SMS with given message body."""

    config = read_config('config.ini')
    account_sid =  config['twilio']['account_sid']
    auth_token  =  config['twilio']['auth_token']
    from_phone  =  config['twilio']['from_phone']
    to_phone    =  config['twilio']['to_phone']

    client = Client(account_sid, auth_token) 
    client.messages.create(from_=from_phone,body=body,to=to_phone)