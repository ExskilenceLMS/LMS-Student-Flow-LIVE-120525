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
from Student_Flow_App import views ,tests ,coding_validation as cv ,AppUsage,StudentProfile as profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('api/clearcache/', AppUsage.clear_blob_ceche),
    # Dashboard URLs
    path('api/studentdashboard/mycourses/<str:student_id>/',       views.fetch_enrolled_subjects),
    path('api/studentdashboard/upcomming/sessions/<str:student_id>/',      views.fetch_live_session),
    path('api/studentdashboard/upcomming/events/<str:Course_id>/',       views.fetch_upcoming_events),
    path('api/studentdashboard/weeklyprogress/<str:student_id>/',       views.get_weekly_progress),
    path('api/studentdashboard/hourspent/<str:student_id>/<str:week>/',       views.fetch_study_hours),
    path('api/studentdashboard/summary/<str:student_id>/',       views.fetch_student_summary),
    path('api/studentdashboard/event/calender/<str:student_id>/',       views.fetch_calendar),
    
    # top navigation and roadmap URLs
    path('api/notifications/<str:student_id>/',       views.fetch_top_navigation),
    path('api/roadmap/<str:student_id>/<str:course_id>/',       views.fetch_roadmap),

    # learning modules URLs
    path('api/student/learningmodules/<str:student_id>/<str:subject>/<str:day_number>/',       views.fetch_learning_modules),
    path('api/student/lessonoverview/<str:student_id>/<str:subject>/<str:day_number>/',       views.fetch_overview_modules),
    path('api/student/practice<str:type>/<str:student_id>/<str:subject>/<str:subject_id>/<str:day_number>/<str:week_number>/<str:subTopic>/',       views.fetch_questions),
    path('api/student/add/days/', views.add_days_to_student),
    path('api/student/practicemcq/submit/', views.submit_MCQ_Question),
    # path('api/student/status/practice<str:type>/<str:student_id>/<str:subject>/<str:day_number>/<str:week_number>/<str:subTopic>/', views.fetch_questions_status),

    # coding Validation URLs
    path('api/student/coding/py/',    cv.run_python),
    path('api/student/coding/ds/', cv.run_pythonDSA),
    path('api/student/coding/sql/', cv.sql_query),
    path('api/student/coding/', views.submition_coding_question),

    # Live Session URLs
    path('api/student/sessions/<str:student_id>/', views.fetch_all_live_session),

    # TEST Details URLs
    path('api/student/testdetails/<str:student_id>/', views.fetch_all_test_details),
    
    # Teckets URLs
    path('api/student/tickets/', views.submit_Tickets),
    path('api/student/tickets/<str:student_id>/', views.fetch_all_tickets),
    path('api/student/ticket/comments/', views.student_side_comments_for_tickets),

    # FAQ URLs
    path('api/student/faq/',views.fetch_FAQ),

    # Profile URLs
    path('api/student/profile/<str:student_id>/', profile.fetch_student_Profile),
    path('api/student/profilespcial/', profile.update_social_media),

    # TESTING URLS
    path('addstudent/',      tests.addStudent),
    path('addstudentactivity/<str:day>/<str:week>/',      tests.addStudetsActivity),
    path('addlivesession/',  tests.addLiveSession),
    path('addappusage/',     tests.addstudent_app_usages),
    path('addsubplan/',   tests.add_course_plane_details),
    path('addnotification/',   tests.add_notification),
    path('addstudentinfo/',   tests.update_student_info),
    path('addparticipants/',   tests.add_participants),
    path('addtestdetails/',   tests.add_test_sction),
]

