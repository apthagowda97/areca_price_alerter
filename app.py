import send_sms
import get_price
from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def test():
    return (get_price.get_price('SHIVAMOGGA'))

if __name__=='__main__':
    app.run()