import areca_price
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


load_dotenv()

proxy_client = TwilioHttpClient(proxy={'http': os.getenv("HTTP_PROXY"), 'https': os.getenv("HTTPS_PROXY")})
client = Client(http_client=proxy_client)

def send_sms(body:str):
    """Send the SMS with given message body."""
    
    from_phone = os.getenv("TWILIO_SMS_FROM")
    to_phone = os.getenv("TWILIO_SMS_TO")
    client.messages.create(from_=from_phone,body=body,to=to_phone)

if __name__=='__main__':
    body = areca_price.get_body(city='SHIVAMOGGA')
    send_sms(body=body)