from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name=models.CharField(max_length=150)
    about=models.CharField(max_length=500)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin=models.BooleanField(default=False)
    joined_at=models.DateTimeField(auto_now_add=True)
    group=models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_members')

    class Meta:
        constraints=[models.UniqueConstraint(fields=['user', 'group'], name='unique_member_constraint')]

    def __str__(self):
        return self.user.username


class GroupMessage(models.Model):
    group=models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    sender=models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.TextField()
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group.name