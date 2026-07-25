from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Chat, Conversation
import json

class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user=self.scope["user"]
        self.group_name=f"user_{self.user.id}"
        if self.user.is_authenticated:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data):
        data=json.loads(text_data)
        chat_id=data.get("chat_id")
        message=data.get("message")

        try:
            chat_obj=await Chat.objects.select_related('user1', 'user2').aget(id=chat_id)
        except Chat.DoesNotExist:
            return

        if self.user.id not in [chat_obj.user1.id, chat_obj.user2.id]:
            return
        await Conversation.objects.acreate(chat=chat_obj, message=message, user=self.user)
        if self.user.id == chat_obj.user1.id:
            receiver=chat_obj.user2
        else:
            receiver=chat_obj.user1

        payload={
            'type':'chat_message',
            'sender_id': self.user.id,
            'chat_id': chat_id,
            'message': message,
        }

        await self.channel_layer.group_send(f"user_{receiver.id}", payload)

        await self.channel_layer.group_send(self.group_name, payload)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sender_id': event["sender_id"],
            'chat_id':event["chat_id"],
            'message':event["message"]
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)