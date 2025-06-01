# from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializers import PostSerializer
from account.models import User
from account.serializers import UserSerializer
from .models import Post
from .forms import PostForm

# Create your views here.
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many = True)

    return JsonResponse(serializer.data, safe = False)

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk = id)
    many_ids = [friend.id for friend in user.friends.all()]
    many_ids.append(id)
    # posts = Post.objects.filter(author_id = id)
    posts = Post.objects.filter(author__in = many_ids)
    post_serializer = PostSerializer(posts, many = True)
    user_serializer = UserSerializer(user)

    # print({'user': user_serializer.data, 'posts': post_serializer.data})

    return JsonResponse({'user': user_serializer.data, 'posts': post_serializer.data}, safe = False)

@api_view(['POST'])
def post_create(request):
    # data = request.data
    form = PostForm(request.data)
    
    if form.is_valid():
        post = form.save(commit = False)
        post.author = request.user
        post.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe = False)

    return JsonResponse({'Hola': 'hello'})
