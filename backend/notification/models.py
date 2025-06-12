import uuid
from django.db import models
from account.models import User
from post.models import Post

# Create your models here.

class Notification(models.Model):

    CHOICES_OF_NOTIFY = [
        ("newfriendreq", "New Friend Request"),
        ("acceptedfriendreq", "Accepted Friend Request"),
        ("rejectedfriendreq", "Rejected Friend Request"),
        ("postlike", "Post Like"),
        ("postcomment", "Post Comment"),
    ]

    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    body = models.TextField()
    is_read = models.BooleanField(default= False)
    notification = models.CharField(max_length= 50, choices= CHOICES_OF_NOTIFY)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, blank= True, null= True)
    create_by = models.ForeignKey(User, related_name= 'created_notify', on_delete= models.CASCADE)
    create_for = models.ForeignKey(User, related_name= 'recieved_notify', on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)
