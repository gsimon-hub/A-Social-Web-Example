from django.urls import path
from .views import post_list, post_create, post_list_profile, post_like, post_detail, post_comment, trend_list, delete_post, report_post

urlpatterns = [
    path('', post_list, name= 'post_list'),
    path('<uuid:pk>/', post_detail, name= 'post_detail'),
    path('<uuid:id>/like/', post_like, name= 'post_like'),
    path('<uuid:pk>/comment/', post_comment, name= 'post_comment'),
    path('<uuid:pk>/delete/', delete_post, name= 'delete_post'),
    path('<uuid:pk>/report/', report_post, name= 'report_post'),
    path('profile/<uuid:id>/', post_list_profile, name= 'post_list_profile'),
    path('create/', post_create, name= 'post_create'),
    path('trends/', trend_list, name= 'trend_list'),
]
