
import json
from channels.generic.websocket import WebsocketConsumer

from .views import respond_to_websockets

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        message = text_data_json['text']
        self.send(text_data=json.dumps({
            'text': message,
            'type': 'text',
            'source': 'CANDIDATE'
        }))

        response = respond_to_websockets(text_data_json)
        # Reformat the response and send it to the HTML to print
        response['source'] = 'BOT'
        self.send(text_data=json.dumps(response))