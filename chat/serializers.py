from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from chat.models import Chat, Conversation
from whoisthis.serializers import UserSerializer
from django.contrib.auth.models import User

class ChatSerializer(ModelSerializer):
    user1=UserSerializer(read_only=True)
    user2=UserSerializer(read_only=True)
    class Meta:
        model=Chat
        fields='__all__'

class ChatCreationSerializer(ModelSerializer):
    user2=PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model=Chat
        fields='__all__'

class ConversationSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Conversation
        fields='__all__'

class ConversationWriteSerializer(ModelSerializer):
    user=PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model=Conversation
        fields=['chat', 'user', 'message']