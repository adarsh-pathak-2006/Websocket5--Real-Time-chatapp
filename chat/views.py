from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from chat.serializers import ChatSerializer, ConversationSerializer, ChatCreationSerializer
from chat.models import Chat, Conversation
from rest_framework.response import Response
from django.db.models import Q


class ChatAPI(APIView):
    def get(self, request):
        data=Chat.objects.filter(user1=request.user)
        serial=ChatSerializer(data, many=True)
        return Response(serial.data, status=200)

    def post(self, request):
        serial=ChatCreationSerializer(data=request.data)
        if serial.is_valid():
            serial.save(user1=request.user)
            return Response(serial.data, status=201)
        else:
            return Response(serial.errors, status=400)

class ConversationAPI(APIView):
    def get(self, request, pk):
        chat_data=get_object_or_404(Chat, Q(user1=request.user) | Q(user2=request.user), id=pk)
        data=Conversation.objects.filter(chat=chat_data, user=request.user)
        serial=ConversationSerializer(data, many=True)
        return Response(serial.data, status=200)