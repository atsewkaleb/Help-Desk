from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

from dj4e import settings




class CustomUser(AbstractUser):
    STATUS = (
        ( 'ict_director', 'ict_director'),
        ( 'team_leader',  'team_leader'),
        ('staff', 'staff'),
        ('client', 'client'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField("Role", max_length=100, choices=STATUS, default='Client', blank=True)
    location = models.CharField(max_length=100, default='')
    department = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.username

User = get_user_model()

class Request(models.Model):
    request_type = models.CharField(max_length=200)
    request_location = models.CharField(max_length=100)
    request_department = models.CharField(max_length=100)
    requester_name = models.CharField(max_length=100)
    requester_email = models.EmailField()
    requester_phone = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)
    assigned_team_leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='team_leader_requests', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'team_leader'}
    )
    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='staff_requests', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'staff'}
    )
    is_completed = models.BooleanField(default=False)
    feed_back = models.TextField(max_length=600, default='', blank=True)

    def __str__(self):
        return f"Request {self.id} - {self.request_type}"

