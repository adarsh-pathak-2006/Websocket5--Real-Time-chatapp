from rest_framework.serializers import ModelSerializer
from group.models import Group, GroupMessage
from whoisthis.serializers import UserSerializer

class GroupSerializer(ModelSerializer):
    members=UserSerializer(read_only=True, many=True)
    class Meta:
        model=Group
        fields='__all__'


class GroupMessageSerializer(ModelSerializer):
    sender=UserSerializer(read_only=True)
    class Meta:
        model=GroupMessage
        fields='__all__'