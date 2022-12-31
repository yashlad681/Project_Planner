from django.urls import path
from . import teams, users, project_boards

urlpatterns = [
    path('users/list', users.UserBase.as_view({'get':'list_users'}), name='users_list'),
    path('users/create', users.UserBase.as_view({'post':'create_user'}), name='create_user'),
    path('users/details',  users.UserBase.as_view({'post':'describe_user'}), name='describe_user'),
    path('users/update',  users.UserBase.as_view({'post':'update_user'}), name='update_user'),
    path('users/teams',  users.UserBase.as_view({'post':'get_user_teams'}), name='get_user_teams'),

    path('teams/list', teams.TeamBase.as_view({'get':'list_teams'}), name='teams_list'),
    path('teams/create', teams.TeamBase.as_view({'post':'create_team'}), name='create_team'),
    path('teams/details',  teams.TeamBase.as_view({'post':'describe_team'}), name='describe_team'),
    path('teams/update',  teams.TeamBase.as_view({'post':'update_team'}), name='update_team'),
    path('teams/add-users',  teams.TeamBase.as_view({'post':'add_users_to_team'}), name='add_users'),
    path('teams/remove-users',  teams.TeamBase.as_view({'post':'remove_users_from_team'}), name='remove_users'),
    path('teams/list-users',  teams.TeamBase.as_view({'post':'list_team_users'}), name='list_team_users'),

    path('boards/list',project_boards.ProjectBoardsBase.as_view({'post':'list_boards'}), name='boards_list'),
    path('boards/create', project_boards.ProjectBoardsBase.as_view({'post':'create_board'}), name='create_board'),
    path('boards/close',  project_boards.ProjectBoardsBase.as_view({'post':'close_board'}), name='close_board'),
    path('boards/create-task', project_boards.ProjectBoardsBase.as_view({'post':'create_task'}), name='create_task'),
    path('boards/update-task-status',  project_boards.ProjectBoardsBase.as_view({'post':'update_task_status'}), name='update_task_status'),
    path('boards/export',  project_boards.ProjectBoardsBase.as_view({'post':'export_board'}), name='export_board'),


]
