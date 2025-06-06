from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm, ProfileForm
from django.shortcuts import get_object_or_404
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendsRequestSerializer


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()
    else:
        message = 'error'

    return JsonResponse({'status': message})

@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data['email']

    if User.objects.exclude(id = user.id).filter(email = email).exists():
        return JsonResponse({'message': 'Email already exists.'})
    else:
        print(request.FILES)
        print(request.POST)
        
        form = ProfileForm(request.POST, request.FILES, instance= user)

        if form.is_valid():
            form.save()
        # user.name = request.data['name']
        # user.email = request.data['email']
        # user.save()
        return JsonResponse({'message': 'Profile Updated.'})

@api_view(['GET'])
def friends(request, pk):
    user = get_object_or_404(User, pk = pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for = user, status = 'sent')

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many = True).data,
        'requests': FriendsRequestSerializer(requests, many = True).data,
    }, safe= False)

@api_view(['POST'])
def friendship_request(request, pk):
    print('send_friendship_request:', pk)

    user = get_object_or_404(User, pk = pk)

    check1 = FriendshipRequest.objects.filter(created_for = request.user, created_by = user)
    check2 = FriendshipRequest.objects.filter(created_for = user, created_by = request.user)
    
    if user != request.user and (not check1 or not check2):
        FriendshipRequest.objects.create(
            created_for = user,
            created_by = request.user
        )

        return JsonResponse({'message': 'bla bla bla created'})

    return JsonResponse({'message': 'Request already fulfilled.'})

@api_view(['POST'])
def handle_request(request, pk, status):
    user = get_object_or_404(User, pk = pk)
    # 'QuerySet' object has no attribute 'save' 🚩
    # friend_request = FriendshipRequest.objects.filter(created_for = request.user, created_by = user)
    friend_request = FriendshipRequest.objects.filter(created_for = request.user).get(created_by = user)
    friend_request.status = status

    friend_request.save()

    if status == 'accepted':
        user.friends.add(request.user)
        user.friends_count = user.friends_count + 1
        user.save()

        request.user.friends_count = request.user.friends_count + 1
        request.user.save()

    return JsonResponse({'handle requests': 'bla bla bla created'})

