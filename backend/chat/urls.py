from django.urls import path
from .views import chat_list, chat_detail, chat_send_message

urlpatterns = [
    path('', chat_list, name= 'chats'),
    path('<uuid:pk>/', chat_detail, name= 'chat_detail'),
    path('<uuid:pk>/send/', chat_send_message, name= 'chat_send_message'),
]
