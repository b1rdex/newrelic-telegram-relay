from flask import Flask, request
from flask_restful import Resource, Api
from telegram import send_telegram_message
import os

app = Flask(__name__)
api = Api(app)

token = os.environ['TG_TOKEN']
chat_id = os.environ['TG_CHAT']

class WebHook(Resource):
    def post(self):
        payload = request.json
        print('Received webhook.')
        print(payload)
        print('Sending message to telegram chat: ' + chat_id)
        state = payload.get('current_state')
        if state == 'open':
            state_title = '🚨 ' + \
                payload.get('event_type') + ' ' + state
        else:
            state_title = '✅ ' + \
                payload.get('event_type') + ' ' + state
        message = "*" + state_title + '*\n' \
            '*Policy*: ' + payload.get('policy_name') + '\n' \
            '*Details*: ' + payload.get('details') + '\n' \
            '*Time*: ' + payload.get('timestamp_utc_string') + '\n' \
            '[](' + payload.get('violation_chart_url') + ')' \
            '[Incident Link](' + payload.get('incident_url') + ')' + '\n'
        send_telegram_message(token, chat_id, message)

        return 'OK'

api.add_resource(WebHook, '/webhook')

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
