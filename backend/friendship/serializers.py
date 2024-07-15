from rest_framework import serializers
from django.contrib.auth import get_user_model

# models
from .models import FriendRequest

# serializers
from accounts.serializers import UserSerializer





class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'created_at']


