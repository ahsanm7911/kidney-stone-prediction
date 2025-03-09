from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='patient_dashboard'),
    path('book-appointment/', views.book_appointment, name='book_appointment_for_patient'),
    path('scan-report/', views.scan_report, name='scan_report_for_patient'),
    path('appointments/', views.appointments, name='appointments_for_patient'),
    path('appointment/<int:doctor_id>/', views.appointment_detail, name='appointment_detail_for_patient'),
    path('settings/', views.settings, name='settings_for_patient')
]
