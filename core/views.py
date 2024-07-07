from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User,Tasks,AssignTasks
from .serializer import UserSerail,TasksSerial,AssignTasksSerial
import jwt
from django.conf import settings
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from datetime import datetime,timedelta
KEYS = getattr(settings, "KEY_", None)


class LoginAPI(APIView):
    def post(self,request,format=None):
        data_=request.data
        uname= data_.get('username')
        password = data_.get('password')

        if uname is None or password is None:
            return Response({'status':False,'message':'username or password should not be null'},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=uname, password=password)
        

        if user is not None:
            payload_ ={'username':uname,'exp':datetime.utcnow() + timedelta(days=1)}

            token = jwt.encode(payload=payload_,
                                   key=KEYS
                                   )
            return Response({'status':True,'message':"login success",'token':token},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'Invalid username or password'},status= status.HTTP_401_UNAUTHORIZED)






class RegisterApi(APIView):
    def post(self,request,format=None):
        data_ = request.data
        uname=data_.get('username')
        password=make_password(data_.get('password'))
        fname=data_.get('first_name')
        lname=data_.get('last_name')
        em=data_.get('email')
        if password is None:
            return Response({"status":False,"message":"password required"},status.status.HTTP_400_BAD_REQUEST)
        data_ = {
            "username":uname,"password":make_password(password),"first_name":fname,"last_name":lname,
            "email":em
        }
        serial = UserSerail(data=data_)
        if serial.is_valid():
            serial.save()
            payload_ ={'username':uname,'exp':datetime.utcnow() + timedelta(days=1)}

            token = jwt.encode(payload=payload_,
                                   key=KEYS
                                   )
            return Response({'status':True,'message':"success",'token':token},status=status.HTTP_200_OK)

        else:
            return Response({"status":False,"message":serial.errors},status=status.HTTP_400_BAD_REQUEST)
    


class CreateTask(APIView):
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            usr= User.objects.get(username= d.get("username"))
            if usr.role != 'admin':
                return Response({'status':False,"message":"Access Denied"},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data_ = request.data

        serial = TasksSerial(data=data_)
        if serial.is_valid():
            serial.save()
            return Response({"status":True,"message":"Task Created successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"status":False,"message":serial.errors},status=status.HTTP_400_BAD_REQUEST)


class GetTask(APIView):
    def get(self,request,pk=None,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            usr= User.objects.get(username= d.get("username"))
            if usr.role != 'admin':
                return Response({'status':False,"message":"Access Denied"},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if pk is not None:
            try:
                ob = Tasks.objects.get(id = pk)
                serail = TasksSerial(ob)
                return Response({"status":True,"message":"success","data":serial.data},status=status.HTTP_200_OK)
            except:
                return Response({"status":False,"message":"Incorrect Id"},status=status.HTTP_400_BAD_REQUEST)
        data = Tasks.objects.all()
        serail = TasksSerial(data,many=True)
        return Response({"status":True,"message":"success","data":serail.data},status=status.HTTP_200_OK)

            


class UpdateTask(APIView):
    def patch(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            usr= User.objects.get(username= d.get("username"))
            if usr.role != 'admin':
                return Response({'status':False,"message":"Access Denied"},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data_ = request.data
        if data_.get("id") is None:
            return Response({"status":False,"message":"Provide Id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            ob = Tasks.objects.get(id=data_.get('id'))
        except:
            return Response({"status":False,"message":"Task not Found"},status=status.HTTP_400_BAD_REQUEST)
        serial = TasksSerial(ob,data=data_,partial=True)
        if serial.is_valid():
            serial.save()
            return Response({'status':True,"data":serial.data,'message':'success'},status=status.HTTP_200_OK)
        else:
            return Response({"status":False,"message":serial.errors},status=status.HTTP_400_BAD_REQUEST)
    


class DeleteTask(APIView):
    def delete(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            usr= User.objects.get(username= d.get("username"))
            if usr.role != 'admin':
                return Response({'status':False,"message":"Access Denied"},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        data_ = request.data
        if data_.get("id") is None:
            return Response({"status":False,"message":"Provide Id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            ob = Tasks.objects.get(id=data_.get('id'))
        except:
            return Response({"status":False,"message":"Task not Found"},status=status.HTTP_400_BAD_REQUEST)

        ob.delete()
        return Response({'status':False,'message':'Task Deleted Successfully'},status=status.HTTP_400_BAD_REQUEST)



class AddTask(APIView):
    def post(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            usr= User.objects.get(username= d.get("username"))
            if usr.role != 'admin':
                return Response({'status':False,"message":"Access Denied"},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data_= request.data

        try:
            usr= User.objects.get(id= data_.get('user_id'))
        except:
            return Response({"status":False,"message":"User Id incorrect"},status=status.HTTP_400_BAD_REQUEST)

        try:
            task= Tasks.objects.get(id= data_.get('task_id'))
        except:
            return Response({"status":False,"message":"Task Id incorrect"},status=status.HTTP_400_BAD_REQUEST)

        AssignTasks.objects.create(user_id=usr,task_id=task)

        return Response({'status':True,"message":"Task created successfully"},status=status.HTTP_200_OK)


class GetAssignTasks(APIView):
    def get(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            usr= User.objects.get(username= d.get("username"))
            if usr.role != 'admin':
                return Response({'status':False,"message":"Access Denied"},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data= AssignTasks.objects.all()
        serial = AssignTasksSerial(data)
        return Response({'status':True,"data":serial.data},status=status.HTTP_200_OK)


class UpdateStatus(APIView):
    def patch(self,request,format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            
        except:
            return Response({'status': False, 'message': 'Token Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        

        data_ = request.data
        
        try:
            t= AssignTasks.objects.get(id= data_.get('task_id'))
        except:
            return Response({"status":False,"message":"Incorrect Id"},status=status.HTTP_400_BAD_REQUEST)

        serial = AssignTasksSerial(t,data=data_,partial=True)

        if serial.is_valid():
            return Response({'status':True,"message":"status updated successfully"},status.HTTP_200_OK)
        else:
            return Response({"status":False,"message":serial.errors},status.HTTP_400_BAD_REQUEST)
