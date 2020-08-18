
from django.urls import path
from .views import register_apiView, login_apiView, home_userView


urlpatterns = [
    path('register/', register_apiView),
    path('login/', login_apiView),
    path('', home_userView),
]
