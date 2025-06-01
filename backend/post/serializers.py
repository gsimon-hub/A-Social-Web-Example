from rest_framework import serializers
from .models import Post
from account.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'likes_total', 'body', 'created_formatted']
