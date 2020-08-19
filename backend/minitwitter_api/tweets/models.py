from django.db import models

# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    tweet_id = models.IntegerField()

    def getTimelineTweets(cls, user):
        pass
