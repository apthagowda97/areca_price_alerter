import areca_price
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


def send_sms(body: str):
    """Send the SMS with given message body."""

    proxy_client = TwilioHttpClient(proxy={"http": os.getenv("HTTP_PROXY"), "https": os.getenv("HTTPS_PROXY")})
    client = Client(http_client=proxy_client)

    from_phone = os.getenv("TWILIO_SMS_FROM")
    to_phone = os.getenv("TWILIO_SMS_TO")
    webhook = os.getenv('TWILIO_WEBHOOK')

    client.messages.create(from_=from_phone, body=body, status_callback=webhook, to=to_phone)

def main():
    load_dotenv()
    body = areca_price.get_body(city="SHIVAMOGGA")
    message = send_sms(body=body)

if __name__ == "__main__":
    main()