from rest_framework import serializers
from .models import Users, Teams, Boards, Tasks
from rest_framework.exceptions import ValidationError


class UsersSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        if self.instance and self.instance.name != value:
            raise ValidationError("You may not edit user name")
        return value


    class Meta:
        model = Users
        fields = ('name', 'display_name', 'creation_time')

class TeamsSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        if self.instance and self.instance.name != value:
            raise ValidationError("You may not edit team name")
        return value
    

    class Meta:
        model = Teams
        fields = ('name', 'description', 'admin', 'creation_time')


class AddUserToTeamSerializer(serializers.ModelSerializer):

    def validate_users(self, value):
        if self.instance and self.initial_data.get('users',[]):
            if len(self.initial_data.get('users')) > 50:
                raise ValidationError("The max users that can be added only up to 50")
        return value

    class Meta:
        model = Teams
        fields = ('users',)

    def update(self, instance, validated_data):
        users = validated_data.pop('users', [])
        instance = super().update(instance, validated_data)

        # Add users to the many-to-many field
        for user in users:
            instance.users.add(user)

        return instance


class RemoveUserFromTeamSerializer(serializers.ModelSerializer):

    def validate_users(self, value):
        if self.instance and self.initial_data.get('users',[]):
            if len(self.initial_data.get('users')) > 50:
                raise ValidationError("The max users that can be removed only up to 50")
        return value

    class Meta:
        model = Teams
        fields = ('users',)

    def update(self, instance, validated_data):
        users = validated_data.pop('users', [])
        instance = super().update(instance, validated_data)

        # Remove users to the many-to-many field
        for user in users:
            instance.users.remove(user)

        return instance


class BoardsSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        if self.instance and self.instance.name != value:
            raise ValidationError("You may not edit board name")
        return value
    

    class Meta:
        model = Boards
        fields = ('name', 'description', 'team', 'creation_time')


class BoardsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Boards
        fields = ('id', 'name')


class TasksSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if self.instance and self.instance.title != value:
            raise ValidationError("You may not edit task title")
        return value
    

    class Meta:
        model = Tasks
        fields = ('title', 'description', 'user', 'board', 'creation_time')

