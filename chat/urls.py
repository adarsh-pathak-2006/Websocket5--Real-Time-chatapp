from django.urls import path
from chat.views import ChatAPI, ConversationAPI

urlpatterns = [
    path('', ChatAPI.as_view(), name='chat_api'),
    path('<int:pk>/', ConversationAPI.as_view(), name='conversation_api'),
]
