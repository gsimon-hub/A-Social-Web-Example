from django.http import JsonResponse
from rest_framework.decorators import api_view
# from django.shortcuts import render
from .serializers import NotificationSerializer
from .models import Notification

# Create your views here.

@api_view(['GET'])
def notifications(request):
    received_notifications = request.user.recieved_notify.filter(is_read = False)
    receive_serializer = NotificationSerializer(received_notifications, many = True)

    return JsonResponse(receive_serializer.data, safe= False)

@api_view(['POST'])
def read_notify(request, pk):
    notify = Notification.objects.filter(create_for = request.user).get(pk = pk)
    notify.is_read = True
    notify.save()

    return JsonResponse({'message': 'notification read'})
