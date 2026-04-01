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
    
     path('dashboardBroker/',views.dashboardBroker,name='dashboardBroker'),
     path('brokerProfile/',views.brokerProfile,name='brokerProfile'),
     path('editBrokerProfile/<int:bid>',views.editBrokerProfile,name='editBrokerProfile'),
     path('updateBrokerProfile/',views.updateBrokerProfile,name='updateBrokerProfile'),
     path('changeBrokerPassword/',views.changeBrokerPassword,name='changeBrokerPassword'),
     path('updateBrokerPassword/',views.updateBrokerPassword,name='updateBrokerPassword'),
    #  path('brokerScheduledProperties/',views.brokerScheduledProperties,name='brokerScheduledProperties'),
    path('scheduledPlots/', views.viewSchdeuledPropertyDetails, name='viewSchdeuledPropertyDetails'),
    path('brokerPropertyBids/<int:pid>/', views.brokerPropertyBids, name='brokerPropertyBids'),
    path('acceptBid/<int:bid_id>/', views.acceptBid, name='acceptBid'),
    path('rejectBid/<int:bid_id>/', views.rejectBid, name='rejectBid'),
     path('propertyDetails/<int:pid>/', views.property_details, name='propertyDetails'),
    path('chat/<int:bid>/', views.view_chat, name='view_chat'),
    path('sendMessage/', views.send_message, name='send_message'),
    path('viewCommissions/', views.viewCommissions, name='viewCommissions'),
    path('uploadBrokerProfileImage/',views.uploadBrokerProfileImage,name='uploadBrokerProfileImage'),
]
