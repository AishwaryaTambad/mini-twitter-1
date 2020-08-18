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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)

    @classmethod
    def get_or_create_token(cls, user):
        user_auth_token, created_flag = cls.objects.get_or_create(
            user=user)

        username = user_auth_token.user.username
        user_auth_token.token = cls.generate_token()
        return user_auth_token.token

    @classmethod
    def generate_token(cls):
        letters = string.ascii_lowercase
        token = ""
        token_length = 25
        for i in range(token_length):
            token += random.choice(letters)
        return token



