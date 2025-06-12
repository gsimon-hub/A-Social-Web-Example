from django.urls import path
from .views import notifications, read_notify

urlpatterns = [
    path('', notifications, name= 'notifications'),
    path('read/<uuid:pk>/', read_notify, name= 'read_notify'),
]