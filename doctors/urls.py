from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='doctor_dashboard'),
    path('appointments/', views.appointments, name='appointments_for_doctor'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail_for_doctor'),
    path('settings/', views.settings, name='settings_for_doctor')
]
