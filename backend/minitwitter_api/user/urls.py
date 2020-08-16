
from django.urls import path
from .views import register_apiView, login_apiView
urlpatterns = [
    path('register/', register_apiView),
    path('login/', login_apiView),
]
