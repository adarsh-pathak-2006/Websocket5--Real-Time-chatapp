from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user1=models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_is_talking')
    user2=models.ForeignKey(User, on_delete=models.CASCADE, related_name='talking_to_who')
    created_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[models.UniqueConstraint(fields=['user1', 'user2'], name='unique_chat_constraint')]

    def __str__(self):
        return self.user1.username
        

class Conversation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    chat=models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='convo')
    message=models.TextField()
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username