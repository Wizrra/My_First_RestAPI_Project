from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class TodoList(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_lists')
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  completed = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.title} - {'Completed' if self.completed else 'Pending'}"
  
class TodoImage(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='images')
  image = models.ImageField(upload_to='todo_images/')
  uploaded_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Image for {self.todo_list.title}"

class userProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
  bio = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Profile of {self.user.username}"