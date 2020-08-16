from django.db import models
from django.contrib.auth.models import User

from random import randint


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_bio = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class UserAuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)

    def createToken(self, user):
        if not self.user:
            self.user = user    
        username = self.user.username
        self.token = username+"_"+str(randint(10**6, 10**7))

    def getToken(self):
        return self.token
