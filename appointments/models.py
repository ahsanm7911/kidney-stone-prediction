from django.db import models
from accounts.models import CustomUser
from doctors.models import Doctor
from patients.models import Patient
from helpers import STATUS_CHOICES
# Create your models here.

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    report = models.FileField(upload_to="reports/", null=True, blank=True) #  Optional 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason_for_visit = models.TextField()
    payment_status = models.BooleanField(default=False) # True if paid, False otherwise

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"
    


