from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Conversation, ConversationMessage

class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only = True, many = True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'users', 'updated_formatted']

class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only = True)
    sent_by = UserSerializer(read_only = True)
    
    class Meta:
        model = ConversationMessage
        fields = ['id', 'created_formatted', 'sent_to', 'sent_by', 'body', ]

class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only = True, many = True)

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'messages', 'updated_formatted']
