from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .api import signup, me, friendship_request, friends, handle_request, edit_profile, edit_password, friend_suggestions


urlpatterns = [
    path('me/', me, name= 'me'),
    path('signup/', signup, name= 'signup'),
    path('friends/suggested/', friend_suggestions, name= 'friend_suggestions'),
    path('friends/<uuid:pk>/', friends, name= 'friends'),
    path('friends/request/<uuid:pk>/', friendship_request, name='friendship_request'),
    path('friends/<uuid:pk>/<str:status>/', handle_request, name='handle_request'),
    path('editprofile/', edit_profile, name= 'edit_profile'),
    path('editpassword/', edit_password, name= 'edit_password'),
    path('login/', TokenObtainPairView.as_view(), name= 'token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name= 'token_refresh'),
]
