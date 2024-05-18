import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class DigitRecognizeConsumer(WebsocketConsumer):
    def connect(self):
        self.task_id = self.scope["url_route"]["kwargs"]["task_id"]
        self.task_group_name = f"group_{self.task_id}"

        # Join task group
        async_to_sync(self.channel_layer.group_add)(
            self.task_group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave task group
        async_to_sync(self.channel_layer.group_discard)(
            self.task_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]

    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name, {"type": "chat.message", "message": message}
    #     )

    # Receive message from room group
    # def chat_message(self, event):
    #     message = event["message"]
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({"message": message}))

    def digit_progress(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "code": event["code"],
                    "data": event["data"],
                }
            )
        )
