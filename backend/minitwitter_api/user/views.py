from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from django.http import JsonResponse

from .serializers import UserDataSerializer, UserSerializer, FollowSerializer
from .models import UserData, UserAuthToken, UserAuthToken, Follow


# Create your views here.
@api_view(['POST'])
def login_apiView(request):
    username = request.data['username']
    password = request.data['password']

    user = authenticate(username=username, password=password)
    if not user:
        try:
            User.objects.get(username=username)
            return Response(data={'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={'error': 'Wrong username'}, status=status.HTTP_400_BAD_REQUEST)

    # userdata = UserData.objects.get(user=user)
    # serializer = UserDataSerializer(userdata)

    auth_token = UserAuthToken.get_or_create_token(user=user)
    response = {}
    response['token'] = auth_token
    return Response(response, status=status.HTTP_202_ACCEPTED)
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
        user_data = UserData.objects.create(user=user, user_bio='')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'Username is present'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def home_userView(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def userFollow_apiView(request):
    token = request.data['token']
    follow_user = User.objects.get(username=request.data['username'])
    user_auth = UserAuthToken.objects.get(token=token)
    Follow.add_following(current_user=user_auth.user, following=follow_user)
    response = {'message': 'follow successful'}

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['POST'])
def userUnfollow_apiView(request):
    token = request.data['token']
    unfollow_user = User.objects.get(username=request.data['username'])
    user_auth = UserAuthToken.objects.get(token=token)
    Follow.delete_following(current_user=user_auth.user,
                            following=unfollow_user)
    response = {'message': 'unfollow successful'}

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['GET'])
def userFollowers_apiView(request):
    token = request.data['token']
    user = UserAuthToken.objects.get(token=token)

    follow_object = Follow.objects.get(current_user=user.user)
    serializer = FollowSerializer(instance=follow_object)

    data = serializer.data
    followers_ids = data['followers']
    response = []
    for id in followers_ids:
        follower = User.objects.get(pk=id)
        serializer = UserSerializer(instance=follower)
        response.append(serializer.data)

    return Response(data={'followers': response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def userFollowing_apiView(request):
    token = request.data['token']
    user = UserAuthToken.objects.get(token=token)

    follow_object = Follow.objects.get(current_user=user.user)
    serializer = FollowSerializer(instance=follow_object)

    data = serializer.data
    followers_ids = data['followings']
    response = []
    for id in followers_ids:
        follower = User.objects.get(pk=id)
        serializer = UserSerializer(instance=follower)
        response.append(serializer.data)

    return Response(data={'followings': response}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def getUserInfo_apiView(request):
    try:
        token = request.data['token']
        username = request.data['username']
        user = User.objects.get(username=username)
    except:
        user = UserAuthToken.objects.get(token=token).user

    response = UserSerializer(instance=user).data
    response['followers_count'], response['following_count'] = Follow.get_follow_count(
        user)
    user_data = UserData.objects.get(user=user)
    response['user_bio'] = UserDataSerializer(user_data).data['user_bio']

    return Response(data=response,status=status.HTTP_200_OK)
