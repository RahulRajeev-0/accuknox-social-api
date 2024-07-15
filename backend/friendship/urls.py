from django.urls import path
from . import views


urlpatterns = [
    path('request/', views.SendFriendRequest.as_view(), name='send-friend-request'),
    path('accept/', views.AcceptFriendRequest.as_view(), name='accept-friend-request'),
    path('reject/', views.RejectFriendRequest.as_view(), name='reject-friend-request'),
    path('pending-request/', views.PendingFriendsRequest.as_view(), name='pending-friend-requests'),
    path('friends-list/', views.UserFriendList.as_view(), name='friends-list'),
]
