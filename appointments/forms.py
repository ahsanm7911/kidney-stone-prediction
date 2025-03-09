from django import forms
from .models import Appointment
from django.core.exceptions import ValidationError

def validate_cancellation_reason(value):
    if len(value) < 100:
        raise ValidationError("Cancellation reason must be at least 100 characters long.")
    

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor']

# New form for doctor appointment actions
class AppointmentActionForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=[('confirm', 'Confirm'), ('cancel', 'Cancel'), ('complete', 'Complete')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Action"
    )
    cancellation_reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Cancellation Reason",
        required=False,
    )
    post_appointment_notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Post-Appointment Notes",
        required=False
    )


    class Meta:
        model = Appointment
        fields = ['cancellation_reason', 'post_appointment_notes']

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        cancellation_reason = cleaned_data.get('cancellation_reason', '')
        post_appointment_notes = cleaned_data.get('post_appointment_notes', '')

        # Validation only applies when action is 'cancel'
        if action == 'cancel':
            if not cancellation_reason:
                raise forms.ValidationError("Please provide a reason for cancellation.")
            if len(cancellation_reason) < 100:
                raise forms.ValidationError("Cancellation reason must be at least 100 characters long.")
        
        # Validation for 'complete' action
        if action == 'complete':
            if not post_appointment_notes:
                raise forms.ValidationError("Please provide post-appointment notes or tips.")
            if len(post_appointment_notes) < 100:
                raise forms.ValidationError("Post-appointment notes must be at least 100 characters long.")
            
        if action == 'confirm':
            cleaned_data['status'] = 'confirmed'
            cleaned_data['cancellation_reason'] = None  # Clear reason if confirming
        elif action == 'cancel':
            cleaned_data['status'] = 'cancelled'
        elif action == 'complete':
            cleaned_data['status'] = 'completed'
            cleaned_data['cancellation_reason'] = None

        # cleaned_data.pop('action') # Removing action field, which is not needed.
        print("Form data after cleaning: ", cleaned_data)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = self.cleaned_data['status']  # Set status explicitly
        instance.cancellation_reason = self.cleaned_data['cancellation_reason']
        instance.post_appointment_notes = self.cleaned_data['post_appointment_notes']
        if commit:
            instance.save()
        return instance
    
# Appointment filter form 
class AppointmentFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('all', 'All'),
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Status"
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="End Date"
    )