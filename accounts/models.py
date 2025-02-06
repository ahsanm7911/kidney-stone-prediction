from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='na')
    
    def __str__(self):
        return self.username