from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from group.models import GroupMessage, Group, Member
from group.serializer import GroupSerializer, GroupMessageSerializer, MemberSerializer
from rest_framework.response import Response


class GroupAPI(APIView):
    def get(self, request):
        data=Group.objects.filter(created_by=request.user)
        serial=GroupSerializer(data, many=True)
        return Response(serial.data, status=200)

    def post(self, request):
        serial=GroupSerializer(data=request.data)
        if serial.is_valid():
            serial.save(created_by=request.user)
            return Response(serial.data, status=201)
        else:
            return Response(serial.errors, status=400)

class GroupMemberAPI(APIView):
    def get(self, request, pk):
        grp_data=get_object_or_404(Group, id=pk)
        if not Member.objects.filter(group=grp_data, user=request.user).exists() and grp_data.created_by != request.user:
            return Response({'error': 'Not a member'}, status=403)
        data=Member.objects.filter(group=grp_data)
        serial=MemberSerializer(data, many=True)
        return Response(serial.data, status=200)

    def post(self, request, pk):
        grp_data=get_object_or_404(Group, created_by=request.user, id=pk)
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
        from django.contrib.auth.models import User
        user_to_add = get_object_or_404(User, id=user_id)
        if Member.objects.filter(group=grp_data, user=user_to_add).exists():
            return Response({'error': 'Already a member'}, status=400)
        Member.objects.create(group=grp_data, user=user_to_add)
        return Response({'success': 'Member added'}, status=201)

class GroupMessageAPI(APIView):
    def get(self, request, pk):
        grp_data=get_object_or_404(Group, id=pk)
        if not Member.objects.filter(group=grp_data, user=request.user).exists() and grp_data.created_by != request.user:
            return Response({'error': 'Not a member'}, status=403)
        data=GroupMessage.objects.filter(group=grp_data)
        serial=GroupMessageSerializer(data, many=True)
        return Response(serial.data, status=200)

    


