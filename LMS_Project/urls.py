"""LMS_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from Student_Flow_App import views 
urlpatterns = [
    path('admin/', admin.site.urls),
    # Dashboard URLs
    path('api/studentdashboard/mycourses/<str:student_id>/',       views.fetch_enrolled_subjects),
    path('api/studentdashboard/upcomming/sessions/<str:student_id>/',      views.fetch_live_session),
    path('api/studentdashboard/upcomming/events/<str:Course_id>/',       views.fetch_upcoming_events),
    # TESTING URLS
    path('addstudent/',      views.addStudent),
    path('addstudentactivity/<str:day>/<str:week>/',      views.addStudetsActivity),
    path('addlivesession/',  views.addLiveSession),
]
