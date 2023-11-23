import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):


    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'message',
            'message': 'Hello world!'
        }))


    def receive(self, text_data):
        pass
    
    def disconnect(self, code):
        pass