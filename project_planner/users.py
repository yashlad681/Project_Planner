from rest_framework.response import Response
from .models import Users
from .serializers import UsersSerializer, TeamsSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
import json

class UserBase(viewsets.ViewSet):
    """
    API class implementation to manage users.
    """

    # function to handle GET request and list records
    @action(detail=False,methods=['get'])
    def list_users(self,request):
        records = Users.objects.all()
        serializer = UsersSerializer(records, many=True)
        return Response(serializer.data)

    # code to handle POST request and create a new user
    @action(detail=False, methods=['post'])
    def create_user(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            return Response({"id" : user_obj.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #code to handle get request and retrieve a specific record
    @action(detail=True, methods=['post'])
    def describe_user(self,request):
        record = get_object_or_404(Users, pk=request.data.get('id'))
        serializer = UsersSerializer(record)
        return Response(serializer.data)

    # code to handle PUT request and update a specific record
    @action(detail=True, methods=['post'])
    def update_user(self, request):
        record = get_object_or_404(Users, pk=request.data.get('id'))
        serializer = UsersSerializer(record, data=request.data.get('user'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # code to handle GET request and retrieve a specific record
    @action(detail=False, methods=['post'])
    def get_user_teams(self, request):
        record = get_object_or_404(Users, pk=request.data.get('id'))
        teams = record.member_teams.all()
        serializer = TeamsSerializer(teams,many=True)
        return Response(serializer.data)
