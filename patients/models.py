from django.db import models
from accounts.models import CustomUser
from helpers import GENDER_CHOICES, validate_dob, calculate_age
# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    dob = models.DateField(validators=[validate_dob])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    blood_group = models.CharField(max_length=5)
    medical_history = models.TextField(blank=True, null=True)
    current_symptoms = models.TextField()
    ongoing_medications = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_number = models.CharField(max_length=15)

    def get_age(self):
        age = calculate_age(self.dob)
        return age
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.gender}"
