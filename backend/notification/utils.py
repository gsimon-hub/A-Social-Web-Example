from .models import Notification
from post.models import Post
from account.models import FriendshipRequest

def create_notification(request, notify, post_id = None, friendrequest_id = None):
    created_for = None

    match notify:
        case "postlike":
            body = f'{request.user.name} liked one of your post'
            post = Post.objects.get(pk = post_id)
            create_for = post.author
        case "postcomment":
            body = f'{request.user.name} commented on one of your post'
            post = Post.objects.get(id = post_id)
            create_for = post.author
        case "newfriendreq":
            body = f'{request.user.name} send you a friend request'
            friendrequest = FriendshipRequest.objects.get(pk = friendrequest_id)
            create_for = friendrequest.created_for
        case "acceptedfriendreq":
            body = f'{request.user.name} accepted you a friend request'
            friendrequest = FriendshipRequest.objects.get(pk = friendrequest_id)
            create_for = friendrequest.created_for
        case "rejectedfriendreq":
            body = f'{request.user.name} rejected you a friend request'
            friendrequest = FriendshipRequest.objects.get(pk = friendrequest_id)
            create_for = friendrequest.created_for
    
    notification = Notification.objects.create(
        body = body,
        notification = notify,
        create_for = create_for,
        create_by = request.user,
        post_id = post_id
    )

    print(f'{notify} notification created')

    return notification
