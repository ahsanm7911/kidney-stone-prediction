from django.urls import path 
from .views import doctor_dashboard, patient_dashboard, choose_role

urlpatterns = [
    path('', choose_role, name='choose_role' ),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('patient/', patient_dashboard, name='patient_dashboard'),
]
