from rest_framework.response import Response
from .models import Users,Teams
from .serializers import (UsersSerializer, TeamsSerializer,RemoveUserFromTeamSerializer,
AddUserToTeamSerializer)
from rest_framework.decorators import action
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
import json

class TeamBase(viewsets.ViewSet):
    """
    API class implementation to manage teams.
    """

    # function to handle GET request and list records
    @action(detail=False,methods=['get'])
    def list_teams(self,request):
        records = Teams.objects.all()
        serializer = TeamsSerializer(records, many=True)
        return Response(serializer.data)

    # code to handle POST request and create a new team
    @action(detail=False, methods=['post'])
    def create_team(self, request):
        serializer = TeamsSerializer(data=request.data)
        if serializer.is_valid():
            team_obj = serializer.save()
            return Response({"id" : team_obj.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #code to handle get request and retrieve a specific record
    @action(detail=True, methods=['post'])
    def describe_team(self,request):
        record = get_object_or_404(Teams, pk=request.data.get('id'))
        serializer = TeamsSerializer(record)
        return Response(serializer.data)

    # code to handle POST request and update a specific record
    @action(detail=True, methods=['post'])
    def update_team(self, request):
        record = get_object_or_404(Teams, pk=request.data.get('id'))
        serializer = TeamsSerializer(record, data=request.data.get('team'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # code to handle POST request and add user to team
    @action(detail=True, methods=['post'])
    def add_users_to_team(self, request):
        record = get_object_or_404(Teams, pk=request.data.get('id'))
        serializer = AddUserToTeamSerializer(record,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # code to handle POST request and remove user to team
    @action(detail=True, methods=['post'])
    def remove_users_from_team(self, request):
        record = get_object_or_404(Teams, pk=request.data.get('id'))
        serializer = RemoveUserFromTeamSerializer(record,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # function to handle GET request and list all team users
    @action(detail=False,methods=['get'])
    def list_team_users(self,request):
        record = get_object_or_404(Teams, pk=request.data.get('id'))
        team_users = record.users.all()
        serializer = UsersSerializer(team_users, many=True)
        return Response(serializer.data)
