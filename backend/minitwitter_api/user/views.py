from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from django.http import JsonResponse

from .serializers import UserDataSerializer, UserSerializer
from .models import UserData, UserAuthToken


# Create your views here.
@api_view(['POST'])
def login_apiView(request):
    username = request.data['username']
    password = request.data['password']

    user = authenticate(username=username, password=password)
    if not user:
        try:
            User.objects.get(username=username)
            return Response(data={'message': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={'message': 'wrong username entered'}, status=status.HTTP_400_BAD_REQUEST)

    user_data = UserData(user=user, user_bio='hp')
    serializer = UserDataSerializer(user_data)

    auth_token, created_flag = UserAuthToken.objects.get_or_create(user=user)
    auth_token.createToken(user)
    response = {'key': auth_token.getToken()}
    return Response([serializer.data, response], status=status.HTTP_202_ACCEPTED)
    # return JsonResponse({'username': 'username', 'password': 'password'})


@api_view(['POST'])
def register_apiView(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    user_name = request.data['username']
    password = request.data['password']

    try:
        user = User.objects.get(username=user_name)
    except:
        user = User.objects.create_user(
            username=user_name, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'username present'}, status=status.HTTP_400_BAD_REQUEST)
