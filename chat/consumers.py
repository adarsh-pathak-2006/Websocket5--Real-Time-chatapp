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

        chat_obj=await Chat.objects.aget(id=chat_id)

        if self.user not in [chat_obj.user1, chat_obj.user2]:
            return
        await Conversation.objects.acreate(chat=chat_obj, message=message, user=self.user)
        if self.user == chat_obj.user1:
            reciever=chat_obj.user2
        else:
            reciever=chat_obj.user1

        await self.channel_layer.group_send(f"user_{reciever.id}", {
            'type':'chat_message',
            'chat_id': chat_id,
            'message': message,
        })

        await self.channel_layer.group_send(self.group_name,{
            'type':'chat_message',
            'chat_id': chat_id,
            'message': message,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'chat_id':event["chat_id"],
            'message':event["message"]
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)