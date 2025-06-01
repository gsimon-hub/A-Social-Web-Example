import uuid
from django.db import models
from django.utils.timesince import timesince
from account.models import User

# Create your models here.

class Like(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    liked_by = models.ForeignKey(User, related_name= 'likes', on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    image = models.ImageField(upload_to= 'post_attachments')
    author = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= 'post_attachments'
    )

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

    likes = models.ManyToManyField(Like, blank= True)
    likes_total = models.IntegerField(default= 0)

    class Meta:
        ordering = ['-created']

    def created_formatted(self):
        return timesince(self.created)

