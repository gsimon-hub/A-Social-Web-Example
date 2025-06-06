import uuid
from django.db import models
from django.utils.timesince import timesince
from account.models import User

# Create your models here.
class Conversation(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    users = models.ManyToManyField(User, related_name= 'conversations')
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)

    def updated_formatted(self):
        return timesince(self.updated)

class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    conversation = models.ForeignKey(Conversation, related_name= 'messages', on_delete= models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name= 'recieved_messages', on_delete= models.CASCADE)
    sent_by = models.ForeignKey(User, related_name= 'sent_messages', on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['created']

    def created_formatted(self):
        return timesince(self.created)
