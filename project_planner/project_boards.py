from rest_framework.response import Response
from .models import Users,Teams,Boards, Tasks
from .serializers import (UsersSerializer, TeamsSerializer,BoardsSerializer, TasksSerializer,
BoardsListSerializer)
from rest_framework.decorators import action
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
import json
from datetime import datetime


class ProjectBoardsBase(viewsets.ViewSet):
    """
    API class implementation to manage Project boards.
    """

    # function to handle POST request and list BOARDS related to the team
    @action(detail=False,methods=['post'])
    def list_boards(self,request):
        team = get_object_or_404(Teams, pk=request.data.get('id'))
        boards = team.boards.all()
        serializer = BoardsListSerializer(boards, many=True)
        return Response(serializer.data)

    # code to handle POST request and create a new board
    @action(detail=False, methods=['post'])
    def create_board(self, request):
        serializer = BoardsSerializer(data=request.data)
        if serializer.is_valid():
            board_obj = serializer.save()
            return Response({"id" : board_obj.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #code to handle post request and close a board
    @action(detail=True, methods=['post'])
    def close_board(self,request):
        record = get_object_or_404(Boards, pk=request.data.get('id'))
        if record.tasks.filter(status__in=[Tasks.IN_PROGRESS,Tasks.OPEN]).exists():
            return Response({'error':'Tasks are not completed'}, status=status.HTTP_400_BAD_REQUEST)
        record.status = Boards.CLOSED
        record.end_time = datetime.now()
        record.save()
        return Response({"id" : record.id,'status':record.get_status_display()}, status=status.HTTP_200_OK)

    # code to handle POST request and create a new task
    @action(detail=False, methods=['post'])
    def create_task(self, request):
        board = get_object_or_404(Boards, pk=request.data.get('board'))
        if board.status != Boards.OPEN:
            return Response({'error':'Tasks can only added to open boards'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            task_obj = serializer.save()
            return Response({"id" : task_obj.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #code to handle post request and update task status
    @action(detail=True, methods=['post'])
    def update_task_status(self,request):
        record = get_object_or_404(Tasks, pk=request.data.get('id'))
        status_dict = {'OPEN':1,'IN_PROGRESS':2,'COMPLETE':3}
        if request.data.get('status') not in status_dict.keys():
            return Response({'status':'Invalid status type'}, status=status.HTTP_400_BAD_REQUEST)
        record.status = status_dict.get(request.data.get('status'))
        record.save()
        return Response({"id" : record.id,'status':record.get_status_display()}, status=status.HTTP_200_OK)

    #code to handle post request and export board data to a txt file
    @action(detail=True, methods=['post'])
    def export_board(self, request):
        # Parse the input request to obtain the board_id
        board_id = request.data.get('id')
        board = get_object_or_404(Boards, pk=board_id)

        # Create a new file in the out folder using the board_name and board_id as the file name
        file_name = f'{board.name}_{board_id}.txt'
        import os
        if not os.path.exists('out'):
            os.makedirs('out')
        out_file = open(f'out/{file_name}', 'w')

        # Write the board data to the file in a presentable format
        out_file.write(f'Board: {board.name}\n')
        out_file.write(f'Status - {board.get_status_display()}\n')
        out_file.write('Tasks:\n')
        for task in board.tasks.all():
            out_file.write(f'\t{task.title} - Assigned to - {task.user.name} - Status - {task.get_status_display()}\n')

        # Close the file
        out_file.close()

        # Return the file name
        return Response({'out_file': file_name}, status=status.HTTP_200_OK)
