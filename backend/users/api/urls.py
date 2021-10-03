"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token_views
app_name = 'users'
urlpatterns = [

    # path('', views.home, name='blog-home'),
    path('user-details/<int:id>/', views.user_view, name='user-view-api'),
    path('user-details/<str:email>/', views.user_view_email, name='user-view-email-api'),    
    path('register', views.registration, name='user-register-api'),
    # path('login', auth_token_views.obtain_auth_token,name='user-login-api'),
    path('login', views.user_login, name='user-login-api'),

    path('user-update', views.user_update, name='user-update-api'),
    path('passwordReset', views.user_password_reset, name='user-reset-api'),

    path('permission', views.user_permission, name='use-update-api'),



]
