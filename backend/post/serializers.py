from rest_framework import serializers
from .models import Post, Comment, Trend, PostAttachment
from account.serializers import UserSerializer

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ['id', 'get_image']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    attachments = AttachmentSerializer(read_only = True, many = True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'likes_total', 'body', 'created_formatted', 'attachments', 'is_private']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'created_formatted']

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    comments = CommentSerializer(read_only = True, many = True)
    attachments = AttachmentSerializer(read_only = True, many = True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'likes_total', 'body', 'created_formatted', 'comments', 'comments_total', 'attachments']

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ['hashTag', 'occurences']
