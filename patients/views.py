from django.shortcuts import render, HttpResponse
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from helpers import format_date, get_time_greeting, is_date_passed
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
    context = {
        'greeting': get_time_greeting()
    }
    return render(request, "patients/overview.html", context)

def appointments(request):
    user = request.user
    context = {}
    if user.is_patient:
        patient = Patient.objects.get(user=user)
        upcoming_appointment = Appointment.objects.filter(patient=patient, status='pending')[0]
        appointment_status = is_date_passed(upcoming_appointment.appointment_date)
        print(f"Appointment Status: ", appointment_status)
        appointment_date = format_date(upcoming_appointment.appointment_date)
        context = {
            'appointment': upcoming_appointment,
            'status': appointment_status,
            'date': appointment_date
        }
    return render(request, "patients/appointments.html", context)

def records(request):
    return render(request, "patients/records.html")

def settings(request):
    return render(request, "patients/settings.html")

