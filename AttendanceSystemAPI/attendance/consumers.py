import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):
      await self.accept()
      self.user = self.scope["user"]

      if self.user and self.user.is_authenticated:
         self.user_id = self.user.id
         await self.channel_layer.group_add(f"{self.user_id}-message", self.channel_name)
         print(f"[WS] User {self.user_id} connected")
      else:
         print("[WS] Anonymous user connected")

   async def disconnect(self, close_code):
      if hasattr(self, "user_id"):
         await self.channel_layer.group_discard(f"{self.user_id}-message", self.channel_name)
         print(f"[WS] User {self.user_id} disconnected")

   # ✅ Nhận message từ WebSocket FE
   async def receive(self, text_data):
      data = json.loads(text_data)
      message_text = data.get("message")

      if self.user and self.user.is_authenticated and message_text:
         await self.save_message(self.user_id, message_text)

         # Gửi lại cho client hoặc group
         response = {
               "status": "received",
               "from": self.user.username,
               "message": message_text
         }
         await self.send(text_data=json.dumps(response))
         print(text_data=json.dumps(response))

   @database_sync_to_async
   def save_message(self, user_id, message_text):
      Message.objects.create(user_id=user_id, message={"message": message_text})

   # ✅ Gửi từ phía server (qua group_send)
   async def send_last_message(self, event):
      if hasattr(self, "user_id"):
         last_msg = await self.get_last_message(self.user_id)
         await self.send(text_data=json.dumps({
               "status": "server_push",
               "message": last_msg
         }))

   @database_sync_to_async
   def get_last_message(self, user_id):
      msg = Message.objects.filter(user_id=user_id).last()
      return msg.message if msg else None