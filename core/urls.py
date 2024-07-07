from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("login",views.LoginAPI.as_view()),
    path("register",views.RegisterApi.as_view()),
    path("create-task",views.CreateTask.as_view()),
    path("get-task-detail",views.CreateTask.as_view()),
    path("get-task-detail/<str:pk>/",views.GetTask.as_view()),
    path('update-task',views.UpdateTask.as_view()),
    path('add-task',views.AddTask.as_view()),
    path('get-task',views.GetTask.as_view()),
    path('update-status',views.UpdateStatus.as_view())
]