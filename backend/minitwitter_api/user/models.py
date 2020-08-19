from django.db import models
from django.contrib.auth.models import User

import random
import string


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_bio = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class UserAuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    token = models.CharField(max_length=300)

    @classmethod
    def get_or_create_token(cls, user):
        user_auth_token, created_flag = cls.objects.get_or_create(
            user=user)

        username = user_auth_token.user.username
        user_auth_token.token = cls.generate_token()
        user_auth_token.save()
        return user_auth_token.token

    @classmethod
    def generate_token(cls):
        letters = string.ascii_lowercase
        token = ""
        token_length = 25
        for i in range(token_length):
            token += random.choice(letters)
        return str(token)


class Follow(models.Model):
    current_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='current_user')
    followers = models.ManyToManyField(User, related_name='followers')
    followings = models.ManyToManyField(User, related_name='followings')

    @classmethod
    def add_follower(cls, current_user, follower):
        obj, created = cls.objects.get_or_create(current_user=current_user)
        obj.followers.add(follower)

    @classmethod
    def add_following(cls, current_user, following):
        obj, created = cls.objects.get_or_create(current_user=current_user)
        obj.followings.add(following)
        cls.add_follower(following, current_user)

    @classmethod
    def delete_follower(cls, current_user, follower):
        obj, created = cls.objects.get_or_create(current_user=current_user)
        obj.followers.remove(follower)

    @classmethod
    def delete_following(cls, current_user, following):
        obj, created = cls.objects.get_or_create(current_user=current_user)
        obj.followings.remove(following)
        cls.delete_follower(following, current_user)

    @classmethod
    def get_follow(cls, user):
        follow_object, created = cls.objects.get_or_create(current_user=user)
        return follow_object.followers.all(), follow_object.followings.all()

    @classmethod
    def get_follow_count(cls, user):
        followers, following = cls.get_follow(user)
        return len(followers), len(following)
