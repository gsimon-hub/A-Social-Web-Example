# from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationMessageSerializer, ConversationDetailSerializer

# Create your views here.

@api_view(['GET'])
def chat_list(request):
    chats = Conversation.objects.filter(users__in = [request.user])
    chats_serializer = ConversationSerializer(chats, many = True)

    return JsonResponse(chats_serializer.data, safe= False)

@api_view(['GET'])
def chat_detail(request, pk):
    chat = Conversation.objects.filter(users__in = [request.user]).get(pk = pk)
    chat_serializer = ConversationDetailSerializer(chat)

    return JsonResponse(chat_serializer.data, safe= False)

@api_view(['POST'])
def chat_send_message(request, pk):
    chat = Conversation.objects.filter(users__in = [request.user]).get(pk = pk)
    for user in chat.users.all():
        if user != request.user:
            sent_to = user
    
    chat_message = ConversationMessage.objects.create(
        conversation = chat,
        body = request.data['body'],
        sent_to = sent_to,
        sent_by = request.user
    )

    message_serializer = ConversationMessageSerializer(chat_message)

    return JsonResponse(message_serializer.data, safe= False)
