import calendar
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from LMS_MSSQLdb_App.models import *
from LMS_Mongodb_App.models import *
from datetime import datetime, timedelta
from django.db.models import Max, F
import json

from LMS_Project.Blobstorage import get_blob
 
@api_view(['GET'])
def addStudetsActivity(request,day,week):
    try:
        obj = students_info.objects.get( student_id = 'Student1',del_row = False)
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
            student_id = 'Student1',
            course_id = new,
            student_firstname = 'TEST',
            student_lastname = 'TEST',
            student_email = 'TEST',
            student_gender = 'TEST',
            student_course_starttime = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            # batch_id = 'TEST',
            college = 'TEST',
            branch = 'TEST',
            address = 'TEST',    
            phone = 'TEST',
            student_score = 'TEST',
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
def fetch_enrolled_subjects(request,student_id):
    try:
        student_data = students_info.objects.get(student_id = student_id,del_row = False)
        enrolled_subjects = course_subjects.objects.filter(course_id = student_data.course_id,del_row = False)
        latest_activities = student_activities.objects.filter(student_id=student_id,del_row=False).values('subject_id__subject_name').annotate(latest_day=Max('activity_day'))
        sub_days_count = {}
        [sub_days_count.update({activity['subject_id__subject_name']:{'day':activity['latest_day']}})for activity in latest_activities]
        # print(sub_days_count)
        responce = []
        for subject in enrolled_subjects:
            subject_data = {}
            subject_data.update({
                "title": subject.subject_id.subject_name,
                "image": subject.path,
                "duration": f"{getdays(subject.start_date)} - {getdays(subject.end_date)}",
                "progress": calculate_progress(subject.start_date,subject.end_date,sub_days_count.get(subject.subject_id.subject_name,{'day':0}),subject.duration_in_days),
            })
            responce.append(subject_data)
        return JsonResponse(responce,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)    
def calculate_progress(start_date, end_date, student_progress,Total_days):
    days = student_progress.get('day')
    response = {
        "student_progress": int(days /int(Total_days) * 100)
    }
    current_date = datetime.utcnow().__add__(timedelta(days=17,hours=5,minutes=30))
    if current_date.date() < start_date.date() :
        response.update({"progress": 0})
        return response
    start_date = datetime.strptime(str(start_date).split('.')[0], "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(str(end_date).split('.')[0], "%Y-%m-%d %H:%M:%S")
    progress =(((current_date - start_date).days / (end_date - start_date).days) * 100)
    response.update({"progress": int(progress) if progress <= 100 else 100})
    return  response

def getdays(date):
       date = datetime.strptime(str(date).split('.')[0], "%Y-%m-%d %H:%M:%S")
       day = int(date.strftime("%d"))
       month = int(date.strftime("%m"))
       if 4 <= day <= 20 or 24 <= day <= 30:
           suffix = "th"
       else:
           suffix = ["st", "nd", "rd"][day % 10 - 1]
       formatted_date =  (f"{day}{suffix} {calendar.month_abbr[month]}")
       return formatted_date

 
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
            student_ids = ['student1'],
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
            student_ids = ['student1','student2'],
            del_row = 'False'
        )
        return HttpResponse("Success")
    except Exception as e:
        print(e)
        return HttpResponse("Failed")
from django.utils import timezone
@api_view(['GET'])
def fetch_live_session(request,student_id):
    try:
        print(student_id)
        current_time = timezone.now() + timedelta(hours=5, minutes=30)
        if timezone.is_naive(current_time):
            current_time = timezone.make_aware(current_time, timezone.get_current_timezone())
        live_session = live_sessions.objects.using('mongodb').filter(
            session_starttime__gte=current_time,
            student_ids__contains = student_id,
            del_row = "False"
            ).order_by('-session_starttime').values_list('session_title','session_starttime')
        responce = [{
            "title":session[0],
            "date":getdays(session[1])+" "+session[1].strftime("%Y")[2:],
            "time":session[1].strftime("%I:%M") + " " + session[1].strftime("%p")}            for session in live_session ]
        return JsonResponse(responce,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
    
@api_view(['GET'])
def fetch_upcoming_events(request,Course_id):
    try:
        print(Course_id)
        current_time = datetime.utcnow() + timedelta(days=0,hours=5, minutes=30)
        blob_data = json.loads(get_blob('LMS_DayWise/Sa_20250306104329.json'))
        response = extract_events(blob_data,current_time)
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
    
def extract_events(blob_data,current_time):
    events = []
    for event in blob_data:
        for i in blob_data.get(event):
            if i.get('topic') == 'Weekly Test' or i.get('topic') == 'Onsite Workshop' or i.get('topic') == 'Internship':
                date = datetime.strptime(str(i.get('date').replace('T',' ')).split('.')[0], "%Y-%m-%d %H:%M:%S") if str(i.get('date')).__contains__('T') else datetime.strptime(str(i.get('date')+" 00:00:00").split('.')[0], "%Y-%m-%d %H:%M:%S")
                events.append({
                    "title":i.get('topic'),
                    'subject':event,
                    "date":getdays(date)+" "+date.strftime("%Y")[2:],
                    "time":date.strftime("%I:%M") + " " + date.strftime("%p"),
                    'datetime':date
                })
    events = sorted(events, key=lambda k: k['datetime'])
    upcoming = [ event for event in events if event['datetime'].date() >= current_time.date()]
    return upcoming


