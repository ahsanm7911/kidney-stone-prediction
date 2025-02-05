from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('login', views.login_page, name='login-page'),
    path('forgot-password', views.forgot_password_page, name='forgot-password-page'),
]