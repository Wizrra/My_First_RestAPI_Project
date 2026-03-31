from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TodoList, TodoImage, userProfile
from .serializers import  TodoListSerializer, TodoImageSerializer, UserProfileSerializer, userSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# generic
from rest_framework import generics

# Create your views here.
class RegisterUser(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = userSerializer
  permission_classes = [permissions.AllowAny]
  
class LoginUser(generics.CreateAPIView):
  permission_classes = [permissions.AllowAny]
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      username = serializer.validated_data['username']
      password = serializer.validated_data['password']
      user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_408_BAD_REQUEST)
  
class LogoutUser(generics.GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
  
class UserProfile(generics.GenericAPIView):
  serializer_class = UserProfileSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    profile, created = userProfile.objects.get_or_create(user=request.user)
    serializer = self.serializer_class(profile)
    return Response(serializer.data)
  
  def put(self, request):
    profile, created = userProfile.objects.get_or_create(user=request.user)
    serializer = self.serializer_class(profile, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class TodoListView(generics.GenericAPIView):
  serializer_class = TodoListSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return TodoList.objects.filter(user=self.request.user)

  def get(self, request):
    todo_lists = self.get_queryset()
    serializer = self.serializer_class(todo_lists, many=True)
    return Response(serializer.data)

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

    serializer = self.serializer_class(todo_item, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoImageView(generics.GenericAPIView):
  serializer_class = TodoImageSerializer
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  class TodoImageView(generics.GenericAPIView):
    serializer_class = TodoImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
      todo_images = TodoImage.objects.filter(todo_list__user=request.user)
      serializer = self.serializer_class(todo_images, many=True)  
      return Response(serializer.data)



