
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_userView),
    path('register/', views.register_apiView),
    path('login/', views.login_apiView),
    path('follow/', views.userFollow_apiView),
    path('unfollow/', views.userUnfollow_apiView),
    path('followers/', views.userFollowers_apiView),
    path('following/', views.userFollowing_apiView),
    path('user/', views.getUserInfo_apiView),
]
