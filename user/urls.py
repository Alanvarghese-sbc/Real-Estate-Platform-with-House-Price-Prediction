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
    
     path('userDashboard/',views.userDashboard,name='userDashboard'),
     path('userProfile/',views.userProfile,name='userProfile'),
     path('editUserProfile/<int:uid>/',views.editUserProfile,name='editUserProfile'),
     path('updateUserProfile/',views.updateUserProfile,name='updateUserProfile'),

     path('changeUserPassword/',views.changeUserPassword,name='changeUserPassword'),
     path('updateUserPassword/',views.updateUserPassword,name='updateUserPassword'),
     path('addProperty/',views.addProperty,name='addProperty'),
     path('saveProperty/',views.saveProperty,name='saveProperty'),

     path('browseProperty/',views.browseProperty,name='browseProperty'),
     path('myProperty/',views.myProperty,name='myProperty'),

     path('editProperty/<int:pid>/',views.editProperty,name='editProperty'),
     path('updateProperty/',views.updateProperty,name='updateProperty'),

     path('deleteProperty/<int:pid>/',views.deleteProperty,name='deleteProperty'),

     path('viewPropertyDetails/<int:pid>/',views.viewPropertyDetails,name='viewPropertyDetails'),

     path('sendPropertyRequest/',views.sendPropertyRequest,name='sendPropertyRequest'),
     path('placeBid/',views.placeBid,name='placeBid'),
     path('myEnquiries/',views.myEnquiries,name='myEnquiries'),
     path('userSendMessage/',views.userSendMessage,name='userSendMessage'),
     path('openChat/<int:bid>/',views.openChat,name='openChat'),
     path('sendUserMessage/',views.send_user_message,name='sendUserMessage'),

     path('uploadProfileImage/',views.uploadProfileImage,name='uploadProfileImage'),

     path('api/predict-price/', views.predict_price_api, name='predict_price_api'),
     
]
