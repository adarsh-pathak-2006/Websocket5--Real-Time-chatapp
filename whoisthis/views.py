from django.shortcuts import render
from whoisthis.serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response


class RegisterAPI(APIView):
    def post(self, request):
        data=RegisterSerializer(data=request.data)
        if data.is_valid():
            f_name=data.validated_data['first_name']
            l_name=data.validated_data['last_name']
            username=data.validated_data['username']
            email=data.validated_data['email']
            password=data.validated_data['password']

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'user_err':'username or email already exists'}, status=400)
            else:
                User.objects.create_user(first_name=f_name, last_name=l_name, username=username, email=email, password=password)
                return Response({ 'registration_success':'user registered' }, status=201)
        else:
            return Response(data.errors, status=400)
        
