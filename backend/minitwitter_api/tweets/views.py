from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

# Create your views here.


@api_view(['GET'])
def tweetsTimeline_apiView(request, *args, **kwargs):
    token = request.data.get('token', None)
    if not None:
        response = {'message': 'User is not valid'}
        return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)
    