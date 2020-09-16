from flask import Flask, request
import send_sms

app = Flask(__name__)

@app.route("/MessageStatus", methods=['POST'])
def incoming_sms():
    
    message_status = request.values.get('MessageStatus', None)
    if message_status == 'undelivered':
        send_sms.main()

    return ('', 204)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Areca Price Alerter.</h1>"

if __name__ == "__main__":
    app.run()