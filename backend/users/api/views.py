from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from users.models import Profile
from users.models import MyLog

from .serializers import (RegisterUserSerializer,
 UserSerializer,
 ProfileSerializer)
from django.core import serializers

# from rest_framework.authtoken.models import Token



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registration(request):
    if request.method == 'POST':
        # deserilize
        serializer = RegisterUserSerializer(data = request.data)
        print('recieved registration: ', request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data ['response'] = 'succefullly registered a new user'
            # ! Log
            MyLog.objects.create(user=request.user, action= 'create_object' ,description=f'{user.username} user created through {request.user.username}')
            # data ['email'] = user.email
            # data ['username'] = user.username
            # token = Token.objects.get(user=user).key
            # data ['token'] = token
        else:
            data = serializer.errors
        return Response(data)


from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate
from django.core import serializers
import re
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_login(request):
    print(" a new request ")
    print(request.data)
    username = request.data["username"]
    password = request.data["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.groups.filter(name = 'App'):
            print("group")
            return Response(status= status.HTTP_404_NOT_FOUND)

        print(user.groups.all())
        print (user.get_all_permissions() )
        response1 = serializers.serialize("json", [user])
        response2 = serializers.serialize("json", user.groups.all())
        response3 = user.get_all_permissions()
        # myperm =response3.pop() 
        # print(myperm)
        # myperm= re.sub('^[a-zA-Z].*\.', '', myperm)
        # permission = Permission.objects.get(codename=myperm)
        # print(permission)
        # permissionsArr[i] = permissionsArr[i].replace("_", ' ').capitalize()
        # i+= 1
        allresponses = [response1,response2,response3]
        # ! Log
        MyLog.objects.create(user=request.user, action= 'login' ,description=f'{user.username} logged in through {request.user.username} ')
        return Response( allresponses )
    else:
        return Response(status= status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request, id):
    try:
        user = User.objects.get(id=id)
        # print(user , "hi")
        # profile = Profile.objects.get(user= user)
    except: 
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response( serializers.serialize("json", [user]))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view_email(request, email):
    try:
        user = User.objects.get(email=email)
        # print(user , "hi")
        # profile = Profile.objects.get(user= user)
    except: 
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response( serializers.serialize("json", [user]))



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request):
    print("updating user")
    try:
        user = User.objects.get(id=request.data["id"])
    except: 
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        user_serializer = UserSerializer(user, data = request.data)
        data = {}
        if user_serializer.is_valid():
            user_serializer.save()
            data['response'] = 'User infomation updated succefully'
            # ! Log
            MyLog.objects.create(user=request.user, action= 'edit_object' ,description=f'{request.user.username} edited user {user.username} info')

            return Response( data=data)
        print(user)
        return Response(user_serializer.errors)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_password_reset(request):
    print("updating user")
    try:
        user = User.objects.get(id=request.data["id"])
    except: 
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = {}
        try:
            password = request.data['password']
            user.set_password(password)
            user.save()
            print('password changed succefully ')
            data['response'] = 'User infomation updated succefully'
            # ! Log
            MyLog.objects.create(user=request.user, action= 'edit_object' ,description=f'{request.user.username} changed user {user.username} password')

            return Response( data=data)
        except:
            data['error'] = 'Process failed'
            return Response(data = data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permission(request):
    print("i exist")
    if request.method == "GET":
        username = request.data["username"]
        permission = request.data["permission"]
        print( username, permission)
        try: 
            hasPermission = User.objects.get(username= username).has_perm(permission)
            print(hasPermission)
            return Response( data =hasPermission )
        except:
            return Response(  data =False)




# @api_view(['POST'])
# def registration(request):

# department - post per department 
# Hr - admin, supervisor ( different access permissions)