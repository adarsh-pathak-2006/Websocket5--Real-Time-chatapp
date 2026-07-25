from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from chat.serializers import ChatSerializer, ConversationSerializer, ChatCreationSerializer
from chat.models import Chat, Conversation
from rest_framework.response import Response
from django.db.models import Q


class ChatAPI(APIView):
    def get(self, request):
        data=Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        serial=ChatSerializer(data, many=True)
        return Response(serial.data, status=200)

    def post(self, request):
        username = request.data.get('username')
        if username:
            from django.contrib.auth.models import User
            try:
                user2 = User.objects.get(username=username)
                # Create a mutable copy of request.data if it's a QueryDict, or just modify it
                if hasattr(request.data, '_mutable'):
                    request.data._mutable = True
                request.data['user2'] = user2.id
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        
        serial=ChatCreationSerializer(data=request.data)
        if serial.is_valid():
            serial.save(user1=request.user)
            return Response(serial.data, status=201)
        else:
            return Response(serial.errors, status=400)

class ConversationAPI(APIView):
    def get(self, request, pk):
        chat_data=get_object_or_404(Chat, Q(user1=request.user) | Q(user2=request.user), id=pk)
        data=Conversation.objects.filter(chat=chat_data)
        serial=ConversationSerializer(data, many=True)
        return Response(serial.data, status=200)