from django.urls import path
from chat.consumers import ConversationConsumer
from group.consumers import GroupChatConsumer

websocket_urlpatterns=[
    path('ws/chat/', ConversationConsumer.as_asgi()),
    path('ws/group/', GroupChatConsumer.as_asgi()),
]