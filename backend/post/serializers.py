from rest_framework import serializers
from .models import Post, Comment, Trend
from account.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'likes_total', 'body', 'created_formatted']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'created_formatted']

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    comments = CommentSerializer(read_only = True, many = True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'likes_total', 'body', 'created_formatted', 'comments', 'comments_total']

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ['hashTag', 'occurences']
