from django.db import models

class Users(models.Model):
    id = models.AutoField(db_column="id", primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)    

    def __str__(self):
        return self.name 

class Teams(models.Model):
    id = models.AutoField(db_column="id", primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    admin = models.ForeignKey(Users,on_delete=models.CASCADE, related_name='admin_teams')
    users = models.ManyToManyField(Users, related_name='member_teams', blank=True)
    creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)    

    def __str__(self):
        return self.name 


class Boards(models.Model):
    OPEN = 1
    CLOSED = 2
    STATUS = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    )
    id = models.AutoField(db_column="id", primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    team = models.ForeignKey(Teams,on_delete=models.CASCADE, related_name='boards',null=True,blank=True)
    status = models.IntegerField(default=OPEN,choices=STATUS)
    creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)    
    end_time = models.DateTimeField(null=True,blank=True)    

    def __str__(self):
        return self.name


class Tasks(models.Model):
    OPEN = 1
    IN_PROGRESS = 2
    COMPLETE = 3
    STATUS = (
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In progress'),
        (COMPLETE, 'Complete'),
    )
    id = models.AutoField(db_column="id", primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    user = models.ForeignKey(Users,on_delete=models.CASCADE, related_name='tasks',null=True,blank=True)
    board = models.ForeignKey(Boards,on_delete=models.CASCADE, related_name='tasks',null=True,blank=True)
    status = models.IntegerField(default=OPEN,choices=STATUS)
    creation_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)    

    def __str__(self):
        return self.title 

