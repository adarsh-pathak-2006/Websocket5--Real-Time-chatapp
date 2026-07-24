from django.urls import path
from group.views import GroupAPI, GroupMemberAPI, GroupMessageAPI

urlpatterns = [
    path('', GroupAPI.as_view(), name='group_api'),
    path('<int:pk>/members/', GroupMemberAPI.as_view(), name='group_member_api'),
    path('<int:pk>/messages/', GroupMessageAPI.as_view(), name='group_message_api'),
]
