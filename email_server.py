import base64
import os

from flask import request, Flask
from flask_restful import Resource, Api
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(
        SendEmail,
        '/api/v1/send_email/',
    )

    return app

class SendEmail(Resource):
    def post(self):
        message_text = request.json['message_text']
        
        service = connect_to_gmail_api()

        raw_message = build_message(message_text)

        (service.users()
           .messages()
           .send(userId='me', body=raw_message)
           .execute())

        return 200
        
def connect_to_gmail_api():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    return service

def build_message(message_text):
    message = MIMEText(message_text)

    message['to'] = os.environ['RECIPIENT_EMAIL']
    message['from'] = 'me'
    message['subject'] = 'Update From Raspberry Pi'
    
    raw = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    return raw

if __name__ == '__main__':
    app = create_app()

    app.run(port=8080)