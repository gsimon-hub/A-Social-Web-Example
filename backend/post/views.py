# from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db.models import Q
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from account.models import User
from account.serializers import UserSerializer
from notification.utils import create_notification
from .models import Post, Like, Comment, Trend
from .forms import PostForm, AttachmentForm

# Create your views here.
@api_view(['GET'])
def post_list(request):
    # posts = Post.objects.all()
    user = request.user
    many_ids = [friend.id for friend in user.friends.all()] + [user.id]
    print(user)
    posts = Post.objects.filter((~Q(author__in = many_ids) & Q(is_private = False)) | Q(author__in = many_ids))

    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains = '#' + trend)
    
    serializer = PostSerializer(posts, many = True)

    return JsonResponse(serializer.data, safe = False)

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk = pk)

    if request.user not in post.author.friends.all() and request.user != post.author and post.is_private == True:
        return JsonResponse({'message': 'This post is private.'})

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    }, safe= False)

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk = id)
    # user = request.user
    # many_ids = [friend.id for friend in user.friends.all()]
    # many_ids.append(id)
    # posts = Post.objects.filter(author_id = id)
    if request.user in user.friends.all():
        posts = Post.objects.filter(author = user)
    else:
        posts = Post.objects.filter(Q(author = user) & Q(is_private = False))
    post_serializer = PostSerializer(posts, many = True)
    user_serializer = UserSerializer(user)

    # print({'user': user_serializer.data, 'posts': post_serializer.data})

    return JsonResponse({'user': user_serializer.data, 'posts': post_serializer.data}, safe = False)

@api_view(['POST'])
def post_create(request):
    # data = request.data
    # form = PostForm(request.data)
    attachment = None
    form = PostForm(request.POST)
    attachmentForm = AttachmentForm(request.POST, request.FILES)

    if attachmentForm.is_valid():
        attachment = attachmentForm.save(commit= False)
        attachment.author = request.user
        attachment.save()
    
    if form.is_valid():
        post = form.save(commit = False)
        post.author = request.user
        post.save()

        # if request.FILES:
        #     print('has files.')

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count += 1
        user.save()

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

        notify = create_notification(request, 'postlike', post_id = post.id)
        
        return JsonResponse({'message': 'ILikeIt'})

@api_view(['POST'])
def post_comment(request, pk):
    post = Post.objects.get(pk = pk)

    comment = Comment.objects.create(body = request.data['body'], author = request.user)
    post.comments.add(comment)
    post.comments_total += 1
    post.save()

    notify = create_notification(request, 'postcomment', post_id = post.id)

    # print(request.data)
    serializer = CommentSerializer(comment, read_only = True)

    return JsonResponse(serializer.data, safe= False)

@api_view(['GET'])
def trend_list(request):
    trends = Trend.objects.all()
    serializers = TrendSerializer(trends, many = True)

    return JsonResponse(serializers.data, safe= False)

