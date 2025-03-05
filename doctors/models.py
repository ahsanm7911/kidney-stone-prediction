from django.db import models
from accounts.models import CustomUser
from helpers import GENDER_CHOICES, validate_dob, calculate_age
import datetime
# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    dob = models.DateField(validators=[validate_dob])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    experience = models.PositiveIntegerField() # Years of experience 
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_days = models.JSONField(default=list) # e.g Mdonay, Wednesday, Friday
    available_start_time = models.TimeField()
    available_end_time = models.TimeField(default=datetime.time(17, 0))
    hospital_name = models.CharField(max_length=255, blank=True, null=True)
    hospital_address = models.TextField(blank=True, null=True)
    online_consultation = models.BooleanField(default=True) # Supports online booking ?
    bio = models.TextField(blank=True, null=True) # Short description about the doctor

    def get_age(self):
        age = calculate_age(self.dob)
        return age 
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"
    



