from django.http import HttpResponse
from django.shortcuts import render
from .models import User

# Create your views here.
def activate_user(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if id and email:
        user = User.objects.get(email= email, id = id)
        user.is_active = True
        user.save()

        return HttpResponse('User activation successed. Go ahead and log in.')
