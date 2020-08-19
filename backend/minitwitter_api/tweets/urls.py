
from django.urls import path
from .views import tweetsTimeline_apiView


urlpatterns = [
    path('detail/<str:tweet_id>/', tweetsTimeline_apiView),
    path('timeline/<str:token>/', tweetsTimeline_apiView),
    path('<str:token>/', tweetsTimeline_apiView),
]
