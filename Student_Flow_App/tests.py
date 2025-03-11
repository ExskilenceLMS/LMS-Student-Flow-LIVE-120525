import json
from django.test import TestCase

# Create your tests here.
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from LMS_MSSQLdb_App.models import *
from LMS_Mongodb_App.models import *
from datetime import datetime, timedelta

@api_view(['GET'])
def addLiveSession(request):
    try:

        obj = live_sessions.objects.using('mongodb').create(
            # session_id = 'Session1',
            session_title = 'Week 1 Python Discussion',
            session_starttime = datetime.utcnow().__add__(timedelta(days=1,hours=5,minutes=30)),
            session_author = 'TEST',
            session_subject = 'subject1',
            session_meetlink = 'TEST',
            session_endtime = datetime.utcnow().__add__(timedelta(days=1,hours=6,minutes=30)),
            session_video_link = 'TEST',
            session_status = 'UPCOMING',
            del_row = 'False'
        )
        obj1 = live_sessions.objects.using('mongodb').create(
            # session_id = 'Session2',
            session_title = 'Week 2 Python Discussion',
            session_starttime = datetime.utcnow().__add__(timedelta(days=1,hours=5,minutes=30)),
            session_author = 'TEST',
            session_subject = 'subject1',
            session_meetlink = 'TEST',
            session_endtime = datetime.utcnow().__add__(timedelta(days=1,hours=6,minutes=30)),
            session_video_link = 'TEST',
            session_status = 'UPCOMING',
            student_ids = ['25MRITCS001'],
            del_row = 'False'
        )
        obj2 = live_sessions.objects.using('mongodb').create(
            # session_id = 'Session3',
            session_title = 'Week 3 Python Discussion',
            session_starttime = datetime.utcnow().__add__(timedelta(days=1,hours=5,minutes=30)),
            session_author = 'TEST',
            session_subject = 'subject1',
            session_meetlink = 'TEST',
            session_endtime = datetime.utcnow().__add__(timedelta(days=1,hours=6,minutes=30)),
            session_video_link = 'TEST',
            session_status = 'UPCOMING',
            student_ids = ['25MRITCS001','student2'],
            del_row = 'False'
        )
        return HttpResponse("Success")
    except Exception as e:
        print(e)
        return HttpResponse("Failed")

@api_view(['GET'])
def addStudetsActivity(request,day,week):
    try:
        obj = students_info.objects.get( student_id = '25MRITCS001',del_row = False)
        sub = subjects.objects.get(subject_id = 'Subject2',del_row = False)
        topoic = topics.objects.get(topic_id = 'Topic1',del_row = False)
        subtop = sub_topics.objects.get(sub_topic_id = 'SubTopic1',del_row = False)
        student = student_activities.objects.create(
            student_id = obj,
            subject_id = sub,
            activity_end_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            activity_week = week,
            activity_day = day,
            activity_topic = topoic,
            activity_subtopic = subtop,
            del_row = False
        )
        return HttpResponse("Success")
    except Exception as e:
        print(e)
        return HttpResponse("Failed")
@api_view(['GET'])
def addStudent(request):
    try:
        track = tracks.objects.create(
            track_id = 'Track1',
            track_name =  'Engineering',
            track_name_searchable = 'engineering',
            track_description = 'TEST',
            created_by = 'TEST',
            created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            modified_by = 'TEST',
            modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            action = 'TEST',
            del_row = False
        )
        sub = subjects.objects.create(
            subject_id = 'Subject1',
            track_id = track,
            subject_name =  'HTML CSS',
            subject_alt_name = 'htmlcss',
            subject_description = 'TEST',
            created_by = 'TEST',
            created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            modified_by = 'TEST',
            modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            action = 'TEST',
            del_row = False
        )
        sub1 = subjects.objects.create(
            subject_id = 'Subject2',
            track_id = track,
            subject_name =  'Data Structures with C++ and Object-Oriented Programming with C++',
            subject_alt_name = 'datastructureswithc++andobject-orientedprogrammingwithc++',
            subject_description = 'TEST',
            created_by = 'TEST',
            created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            modified_by = 'TEST',
            modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            action = 'TEST',
            del_row = False
        )
        sub2 = subjects.objects.create(
            subject_id = 'Subject3',
            track_id = track,
            subject_name =  'Data Structures and Algorithms',
            subject_alt_name = 'datastructuresandalgorithms',
            subject_description = 'TEST',
            created_by = 'TEST',
            created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            modified_by = 'TEST',
            modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            action = 'TEST',
            del_row = False
        )
        sub3 = subjects.objects.create(
            subject_id = 'Subject4',
            track_id = track,
            subject_name =  'SQL',
            subject_alt_name = 'sql',
            subject_description = 'TEST',
            created_by = 'TEST',
            created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            modified_by = 'TEST',
            modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            action = 'TEST',
            del_row = False
        )
        topic = topics.objects.create(
            topic_id = 'Topic1',
            subject_id = sub,
            topic_name =  'TEST',
            topic_alt_name = 'TEST',
            topic_description = 'TEST',
            created_by = 'TEST',
            created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            modified_by = 'TEST',
            modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            action = 'TEST',
            del_row = False
        )
        subtopic = sub_topics.objects.create(
            sub_topic_id = 'SubTopic1',
            topic_id = topic,
            sub_topic_name =  'TEST',
            sub_topic_description = 'TEST',
            notes = 1,
            videos = 1,
            mcq = 1,
            coding = 1,
            del_row = False
        )
        new = courses.objects.create(
            course_id = 'Course1',
            # track_id = "None",
            course_name =  'Full Stack Web Development',
            course_description = 'TEST',
            course_level = 'TEST',
            created_by = 'TEST',
            created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            modified_by = 'TEST',
            modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            action = 'TEST',
            del_row = False
        )
        course_subject = course_subjects.objects.create(
            course_id = new,
            subject_id = sub,
            duration_in_days = '10',
            start_date = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            end_date = datetime.utcnow().__add__(timedelta(days=10,hours=5,minutes=30)),
            is_mandatory = True,
            path = 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            del_row = False
        )
        course_subject1 = course_subjects.objects.create(
            course_id = new,
            subject_id = sub1,
            duration_in_days = '10',
            start_date = datetime.utcnow().__add__(timedelta(days=10,hours=5,minutes=30)),
            end_date = datetime.utcnow().__add__(timedelta(days=20,hours=5,minutes=30)),
            is_mandatory = True,
            path = 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            del_row = False
        )
        course_subject2 = course_subjects.objects.create(
            course_id = new,
            subject_id = sub2,
            duration_in_days = '10',
            start_date = datetime.utcnow().__add__(timedelta(days=20,hours=5,minutes=30)),
            end_date = datetime.utcnow().__add__(timedelta(days=30,hours=5,minutes=30)),
            is_mandatory = True,
            path = 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            del_row = False
        )
        course_subject3 = course_subjects.objects.create(
            course_id = new,
            subject_id = sub3,
            duration_in_days = '10',
            start_date = datetime.utcnow().__add__(timedelta(days=30,hours=5,minutes=30)),
            end_date = datetime.utcnow().__add__(timedelta(days=40,hours=5,minutes=30)),
            is_mandatory = True,
            path = 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            del_row = False
        )
        std = students_info.objects.create(
            student_id = '25MRITCS001',
            course_id = new,
            student_firstname = 'Raj Kumari',
            student_lastname = 'P',
            student_email = 'TEST',
            student_gender = 'TEST',
            student_course_starttime = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            # batch_id = 'TEST',
            college = 'TEST',
            branch = 'TEST',
            address = 'TEST',    
            phone = 'TEST',
            student_score = 0,
            student_type = 'TEST',
            linkedin = 'TEST',
            leetcode = 'TEST',
            hackerrank = 'TEST',
            del_row = False
        )
        return HttpResponse("Added Successfully")
    except Exception as e:
        print(e)
        return HttpResponse("Failed")

@api_view(['GET'])
def addstudent_app_usages(request):
    try:
        std = student_app_usage.objects.create(
            student_id = '25MRITCS001',
            # app_name = 'TEST',
            logged_in = datetime.utcnow().__add__(timedelta(days=0,hours=5,minutes=30)),
            logged_out = datetime.utcnow().__add__(timedelta(days=0,hours=8,minutes=30)),
            del_row = False
        )
        return HttpResponse("Added Successfully")
    except Exception as e:
        print(e)
        return HttpResponse("Failed")
@api_view(['POST'])
def add_course_plane_details(request):
    try:
        data = json.loads(request.body)

        course = courses.objects.get(course_id = 'Course1' ,del_row = False)
        sub = subjects.objects.get(subject_id = 'Subject4' ,del_row = False)
        for i in range(data['day']):
            week = int(i/7)+1
            course_plan_detail = course_plan_details.objects.create(
                course_id = course,
                subject_id = sub,
                day = i+1,
                content_type = 'study' if (i+1)%7 != 0 else 'weekly test',
                week = week,
                day_date = datetime.utcnow().__add__(timedelta(days=i,hours=5,minutes=30)),
                duration_in_hours = data['duration'],
                del_row = False
            )
        return HttpResponse("Added Successfully")
    except Exception as e:
        print(e)
        return HttpResponse("Failed")
@api_view(['GET'])
def add_notification(request):
    try:
        std = notification.objects.using('mongodb').create(
            notification_title = 'TEST',
            notification_message = 'TEST',
            notification_timestamp = datetime.utcnow().__add__(timedelta(days=0,hours=5,minutes=30)),
            status = 'U',
            student_id = '25MRITCS001',
            del_row = False
        )
        return HttpResponse("Added Successfully")
    except Exception as e:
        print(e)
        return HttpResponse("Failed")
@api_view(['GET'])
def update_student_info(request):
    try:
        new = courses.objects.get(course_id = 'Course1',del_row = False)
        # create(
        #     course_id = 'Course0001',
        #     # track_id = "None",
        #     course_name =  'Full Stack Web Development',
        #     course_description = 'TEST',
        #     course_level = 'TEST',
        #     created_by = 'TEST',
        #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
        #     modified_by = 'TEST',
        #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
        #     action = 'TEST',
        #     del_row = False
        # )
        std = students_info.objects.get(student_id = '25MRITCS001',del_row = False)
        std.course_id = new
        std.student_score = 50
        std.save()
        return HttpResponse("Updated Successfully")
    except Exception as e:
        print(e)
        return HttpResponse("Failed")