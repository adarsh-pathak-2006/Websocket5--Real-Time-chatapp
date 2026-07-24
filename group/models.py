from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name=models.CharField(max_length=150)
    about=models.CharField(max_length=500)
    user=models.ManyToManyField(User, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupMessage(models.Model):
    group=models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.TextField()
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group.name