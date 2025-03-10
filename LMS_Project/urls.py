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
from Student_Flow_App import views ,tests 
urlpatterns = [
    path('admin/', admin.site.urls),
    # Dashboard URLs
    path('api/studentdashboard/mycourses/<str:student_id>/',       views.fetch_enrolled_subjects),
    path('api/studentdashboard/upcomming/sessions/<str:student_id>/',      views.fetch_live_session),
    path('api/studentdashboard/upcomming/events/<str:Course_id>/',       views.fetch_upcoming_events),
    path('api/studentdashboard/weeklyprogress/<str:student_id>/',       views.get_weekly_progress),
    path('api/studentdashboard/hourspent/<str:student_id>/<str:week>/',       views.fetch_study_hours),
    path('api/studentdashboard/summary/<str:student_id>/',       views.fetch_student_summary),
    path('api/studentdashboard/event/calender/<str:student_id>/',       views.fetch_calendar),
    # top navigation
    path('api/notifications/<str:student_id>/',       views.fetch_top_navigation),
    path('api/roadmap/<str:student_id>/<str:course_id>/',       views.fetch_roadmap),
    # TESTING URLS
    path('addstudent/',      tests.addStudent),
    path('addstudentactivity/<str:day>/<str:week>/',      tests.addStudetsActivity),
    path('addlivesession/',  tests.addLiveSession),
    path('addappusage/',     tests.addstudent_app_usages),
    path('addsubplan/',   tests.add_course_plane_details),
    path('addnotification/',   tests.add_notification),
    path('addstudentinfo/',   tests.update_student_info),
]
