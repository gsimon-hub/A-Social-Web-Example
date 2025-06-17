import uuid
from django.conf import settings
from django.db import models
from django.utils.timesince import timesince
from account.models import User

# Create your models here.

class Like(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    liked_by = models.ForeignKey(User, related_name= 'likes', on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)

class Comment(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    body = models.TextField(null= True, blank= True)
    author = models.ForeignKey(User, related_name= 'comments', on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['-created']

    def created_formatted(self):
        return timesince(self.created)

class PostAttachment(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    image = models.ImageField(upload_to= 'post_attachments')
    author = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= 'post_attachments'
    )

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return ''

class Post(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    body = models.TextField(blank= True, null= True)
    attachments = models.ManyToManyField(PostAttachment, blank= True)
    author = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= 'posts'
    )
    created = models.DateTimeField(auto_now_add= True)

    is_private = models.BooleanField(default= False)
    reported_by_users = models.ManyToManyField(User, related_name= 'reported_posts', blank= True)

    likes = models.ManyToManyField(Like, blank= True)
    likes_total = models.IntegerField(default= 0)

    comments = models.ManyToManyField(Comment, blank= True)
    comments_total = models.IntegerField(default= 0)

    class Meta:
        ordering = ['-created']

    def created_formatted(self):
        return timesince(self.created)

class Trend(models.Model):
    hashTag = models.CharField(max_length= 255)
    occurences = models.IntegerField()
