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
from django.urls import path
from . import views

urlpatterns = [
    
     path('dashboardAdmin/',views.dashboardAdmin,name='dashboardAdmin'),
     path('changePassword/',views.changePassword,name='changePassword'),
     path('updatePassword/',views.updatePassword,name='updatePassword'),
     path('broker/',views.broker,name='broker'),
     path('saveBroker/',views.saveBroker,name='saveBroker'),
     path('editBroker/<int:bid>',views.editBroker,name='editBroker'),
     path('updateBroker/',views.updateBroker,name='updateBroker'),
     path('deleteBroker/<int:bid>',views.deleteBroker,name='deleteBroker'),
     path('registered_users/',views.registered_users,name='registered_users'),
     path('viewUserProperties/',views.viewUserProperties,name='viewUserProperties'),
     path('viewUserPropertyDetails/<int:pid>',views.viewUserPropertyDetails,name='viewUserPropertyDetails'),
     path('viewPropertyLocation/<int:pid>',views.viewPropertyLocation,name='viewPropertyLocation'),
     path('assignBroker/<int:pid>',views.assignBroker,name='assignBroker'),
     path('assignBrokerTOProperty/',views.assignBrokerTOProperty,name='assignBrokerTOProperty'),
     path('replaceBrokerForProperty/',views.replaceBrokerForProperty,name='replaceBrokerForProperty'),
     path('deAssignBroker/',views.deAssignBroker,name='deAssignBroker'),
     path('viewBrokerCommissions/',views.viewBrokerCommissions,name='viewBrokerCommissions'),
     path('viewPropertyRequest/',views.viewPropertyRequest,name='viewPropertyRequest'),
     path('request_details/<int:pid>',views.request_details,name='request_details'),
     path('contact-messages/', views.view_contact_messages, name='viewContactMessages')

]
