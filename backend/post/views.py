# from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from account.models import User
from account.serializers import UserSerializer
from .models import Post, Like, Comment, Trend
from .forms import PostForm

# Create your views here.
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()

    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains = '#' + trend)
    
    serializer = PostSerializer(posts, many = True)

    return JsonResponse(serializer.data, safe = False)

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk = pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    }, safe= False)

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

@api_view(['POST'])
def post_like(request, id):
    post = Post.objects.get(pk = id)
    # like = Like.objects.create(liked_by = request.user)
    if post.likes.filter(liked_by = request.user).exists():
        # print(f'Already exists: {post.likes.filter(liked_by = request.user).exists()}')
        post.likes.filter(liked_by = request.user).delete()
        post.likes_total -= 1
        post.save()
        return JsonResponse({'message': 'REMOVED'})
    else:
        like = Like.objects.create(liked_by = request.user)
        # post.likes.add(Like(liked_by = request.user)) 🚩FAILED
        post.likes.add(like)
        post.likes_total += 1
        post.save()

        return JsonResponse({'message': 'ILikeIt'})

@api_view(['POST'])
def post_comment(request, pk):
    post = Post.objects.get(pk = pk)

    comment = Comment.objects.create(body = request.data['body'], author = request.user)
    post.comments.add(comment)
    post.comments_total += 1
    post.save()

    # print(request.data)
    serializer = CommentSerializer(comment, read_only = True)

    return JsonResponse(serializer.data, safe= False)

@api_view(['GET'])
def trend_list(request):
    trends = Trend.objects.all()
    serializers = TrendSerializer(trends, many = True)

    return JsonResponse(serializers.data, safe= False)

