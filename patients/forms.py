from django import forms

class PatientProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of Birth",
        required=False
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        label="Gender",
        required=False
    )
    height = forms.FloatField(label="Height (cm)", required=False)
    weight = forms.FloatField(label="Weight (kg)", required=False)
    blood_group = forms.ChoiceField(
        choices=[('', 'Select Blood Group')] + [
            ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
        ],
        label="Blood Group",
        required=False
    )
    medical_history = forms.CharField(widget=forms.Textarea, label="Medical History", required=False)
    current_symptoms = forms.CharField(widget=forms.Textarea, label="Current Symptoms", required=False)
    ongoing_medications = forms.CharField(widget=forms.Textarea, label="Ongoing Medications", required=False)
    emergency_contact_name = forms.CharField(max_length=100, label="Emergency Contact Name", required=False)
    emergency_contact_number = forms.CharField(max_length=15, label="Emergency Contact Number", required=False)