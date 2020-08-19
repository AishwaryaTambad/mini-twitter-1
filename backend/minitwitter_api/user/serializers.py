from rest_framework import serializers
from .models import UserData, Follow
from django.contrib.auth.models import User


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['user_bio', ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
