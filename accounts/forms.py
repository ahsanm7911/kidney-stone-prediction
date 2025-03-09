from allauth.account.forms import SignupForm
from django import forms 
from .models import CustomUser
from doctors.models import Doctor
from patients.models import Patient 
from helpers import DAY_CHOICES, TIME_SLOTS, GENDER_CHOICES, BLOOD_GROUP_CHOICES
import datetime


class CustomSignupForm(SignupForm):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    
    def save(self, request):
        user = super().save(request)
        return user
    
class DoctorForm(forms.ModelForm):
    available_days = forms.MultipleChoiceField(
        choices=DAY_CHOICES, widget=forms.CheckboxSelectMultiple
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    available_start_time = forms.ChoiceField(choices=TIME_SLOTS, widget=forms.Select(attrs={'class': 'form-select'}), label="Start Time")
    available_end_time = forms.ChoiceField(choices=TIME_SLOTS, widget=forms.Select(attrs={'class': 'form-select'}), label="End Time")
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date of Birth*"
    )

    class Meta:
        model = Doctor 
        fields = ['dob', 'gender', 'specialization', 'license_number', 'experience', 'consultation_fee', 'available_days', 'available_start_time', 'available_end_time', 'hospital_name', 'hospital_address', 'online_consultation', 'bio']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('available_start_time')
        end_time = cleaned_data.get('available_end_time')

        if start_time and end_time:
            start_time = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
            end_time = datetime.datetime.strptime(end_time, '%H:%M:%S').time()

            if start_time >= end_time:
                raise forms.ValidationError("End time must be later than start time.")
        return cleaned_data

class PatientForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Date of Birth*"
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    height = forms.FloatField(label="Height in cm", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(label="Weight in kg", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Patient 
        fields = ['dob', 'gender', 'height', 'weight', 'blood_group', 'medical_history', 'current_symptoms', 'ongoing_medications', 'emergency_contact_name', 'emergency_contact_number']
        