from rest_framework.serializers import ModelSerializer
from group.models import Group, GroupMessage, Member
from whoisthis.serializers import UserSerializer

class MemberSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Member
        fields='__all__'

class GroupSerializer(ModelSerializer):
    group_members=MemberSerializer(read_only=True, many=True)
    class Meta:
        model=Group
        fields='__all__'


class GroupMessageSerializer(ModelSerializer):
    sender=UserSerializer(read_only=True)
    class Meta:
        model=GroupMessage
        fields='__all__'