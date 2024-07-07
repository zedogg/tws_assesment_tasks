from .models import Tasks,AssignTasks,User
from rest_framework import serializers


class TasksSerial(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields='__all__'


class AssignTasksSerial(serializers.ModelSerializer):
    class Meta:
        model=AssignTasks
        fields='__all__'

class UserSerail(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
