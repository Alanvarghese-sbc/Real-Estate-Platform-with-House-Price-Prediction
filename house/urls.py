"""
URL configuration for house project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from . import view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',view.home,name='home'),
     path('login/',view.login,name='login'),
    #  path('admin/',view.adminDashboard,name='admin'),
     path('administrator/',include('administrator.urls')) ,
     path('check_login/',view.check_login,name='check_login'),
     path('register/',view.register,name='register'),
     path('register_user/',view.register_user,name='register_user'),

     path('broker/',include('broker.urls')) ,
     path('user/',include('user.urls')) ,

     path('logout/',view.logout,name='logout'),
     path('forgot_password/', view.forgot_password, name='forgot_password'),
     path('sendOtp/', view.sendOtp, name='sendOtp'),
     path('verify_otp/', view.verify_otp, name='verify_otp'),
     path('reset_password/',view.reset_password, name='reset_password'),
     path('changePassword',view.changeLoginPassword,name='changeLoginPassword'),
     path('contact/',view.contact_view,name='contact'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

