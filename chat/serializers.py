from rest_framework.serializers import ModelSerializer
from chat.models import Chat, Conversation
from whoisthis.serializers import UserSerializer

class ChatSerializer(ModelSerializer):
    user1=UserSerializer(read_only=True)
    user2=UserSerializer(read_only=True)
    class Meta:
        model=Chat
        fields='__all__'

class ConversationSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Conversation
        fields='__all__'