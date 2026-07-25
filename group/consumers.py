import json
from channels.generic.websocket import AsyncWebsocketConsumer
from group.models import GroupMessage, Group, Member
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class GroupChatConsumer(AsyncWebsocketConsumer):
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
        sender_id=self.user.id
        message=data.get("message")
        group_id=data.get("group_id")

        is_member = await Member.objects.filter(user_id=sender_id, group_id=group_id).aexists()
        group_exists = await Group.objects.filter(id=group_id).aexists()
        if is_member and group_exists:
            grp_obj = await Group.objects.aget(id=group_id)
            await GroupMessage.objects.acreate(sender=self.user, message=message, group=grp_obj)

            payload={
                'type':'chat_message',
                'message':message,
                'group_id':group_id,
                'sender_id':self.user.id,
            }               

            members = await sync_to_async(lambda: list(grp_obj.group_members.all()))()

            for member in members:
                await self.channel_layer.group_send(f"user_{member.user_id}", payload)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event["message"],
            'group_id': event["group_id"],
            'sender_id': event["sender_id"]
        }))
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)