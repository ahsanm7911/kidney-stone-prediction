from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from appointments.forms import AppointmentFilterForm
from accounts.forms import PatientForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from helpers import format_date, get_time_greeting, is_date_passed
from datetime import datetime
# Create your views here.

def book_appointment(request):
    doctors = Doctor.objects.all()
    if request.method == "POST":
        print(f"Form Data: {request.POST['doctor_id']}")
    context = {
        'doctors': doctors
    }
    return render(request, "patients/appointment_booking.html", context)

def scan_report(request):
    return render(request, "patients/scan_report.html")

def overview(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        return "Patient profile doesnot exists for this user."
    
    # Calculate age (using model method)
    age = patient.get_age()

    # Calculate BMI
    height_m = patient.height / 100  # Convert cm to m
    bmi = patient.weight / (height_m ** 2) if height_m > 0 else 0
    bmi_category = ""
    bmi_recommendation = ""
    if bmi < 18.5:
        bmi_category = "Underweight"
        bmi_recommendation = "Consider consulting a nutritionist to gain healthy weight."
    elif 18.5 <= bmi < 25:
        bmi_category = "Normal"
        bmi_recommendation = "Maintain your healthy lifestyle!"
    elif 25 <= bmi < 30:
        bmi_category = "Overweight"
        bmi_recommendation = "Consider a balanced diet and exercise plan."
    else:
        bmi_category = "Obese"
        bmi_recommendation = "Consult a healthcare provider for weight management."

    # Symptom-based recommendation (basic example)
    symptoms = patient.current_symptoms.lower()
    symptom_recommendation = ""
    if "fever" in symptoms or "pain" in symptoms or "cough" in symptoms:
        symptom_recommendation = "Schedule an appointment if symptoms persist or worsen."

    # Medications
    medications = patient.ongoing_medications.split(",") if patient.ongoing_medications else []
    medication_count = len([m for m in medications if m.strip()])
    medication_note = "Ensure timely refills for your medications." if medication_count > 0 else ""

    # Appointment stats
    today = datetime.today().date()
    appointments = patient.appointments.all()
    total_appointments = appointments.count()
    upcoming_appointments = appointments.filter(appointment_date__gte=today, status__in=['pending', 'confirmed']).count()
    pending_appointments = appointments.filter(status='pending').count()
    confirmed_appointments = appointments.filter(status='confirmed').count()
    completed_appointments = appointments.filter(status='completed').count()
    cancelled_appointments = appointments.filter(status='cancelled').count()
    last_appointment = appointments.order_by('-appointment_date').first()


    context = {
        'greeting': get_time_greeting(),
        'patient': patient,
        'age': age,
        'bmi': round(bmi, 1),
        'bmi_category': bmi_category,
        'bmi_recommendation': bmi_recommendation,
        'symptom_recommendation': symptom_recommendation,
        'medications': medications,
        'medication_count': medication_count,
        'medication_note': medication_note,
        'total_appointments': total_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'last_appointment': last_appointment,
    }
    return render(request, "patients/overview.html", context)

def appointments(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        return "Patient profile doesnot exists for this user."
    
    # Filter form
    filter_form = AppointmentFilterForm(request.GET or None)
    appointments = patient.appointments.all()

    if filter_form.is_valid():
        status = filter_form.cleaned_data['status']
        start_date = filter_form.cleaned_data['start_date']
        end_date = filter_form.cleaned_data['end_date']

        if status and status != 'all':
            appointments = appointments.filter(status=status)
        if start_date:
            appointments = appointments.filter(appointment_date__gte=start_date)
        if end_date:
            appointments = appointments.filter(appointment_date__lte=end_date)


    context = {
        'patient': patient, 
        'appointments': appointments, 
        'filter_form': filter_form
    }
    return render(request, 'patients/appointments.html', context)

@login_required
def appointment_detail(request, doctor_id):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        return "No profile exists for this patient."
    
    # Fetch the doctor and ensure the patient has an appointment with them
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if not Appointment.objects.filter(patient=patient, doctor=doctor).exists():
        return redirect('appointments')  # Prevent unauthorized access
    
    return render(request, 'patients/doctor_detail.html', {
        'doctor': doctor,
    })

def settings(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        patient = Patient(user=request.user)
        patient.save()
    
    # Initialize both forms 
    profile_form = PatientForm(instance=patient)

    # Check if user has a usable password 
    has_password = request.user.has_usable_password()
    if has_password:
        password_form = PasswordChangeForm(user=request.user)
        password_form.fields['old_password'].widget.attrs.pop('autofocus', None)
    else:
        password_form = SetPasswordForm(user=request.user)


    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = PatientForm(request.POST, instance=patient)
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            if profile_form.is_valid() and first_name and last_name:
                # Update CustomUser fields
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()

                # Save patient form 
                profile_form.save()
                messages.success(request, "Your profile has been updated successfully.")
            else:
                if not first_name or not last_name:
                    messages.error(request, "First name and last name are required.")

        elif 'change_password' in request.POST: # Password change submission
            if has_password:
                password_form = PasswordChangeForm(user=request.user, data=request.POST)
                password_form.fields['old_password'].widget.attrs.pop('autofocus', None)
            else:
                password_form = SetPasswordForm(user=request.user, data=request.POST)
            
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user) # Keep user logged in.
                messages.success(request, f"Your password has been {'change' if has_password else 'set'} successfully!")
                return redirect("settings_for_patient")
            else:
                messages.error(request, "Please correct the errors below.")
    context = {
        'profile_form': profile_form, 
        'password_form': password_form,
        'patient': patient, 
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'has_password': has_password
    }
    return render(request, "patients/settings.html", context)

