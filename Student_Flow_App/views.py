import calendar
from itertools import count
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from LMS_MSSQLdb_App.models import *
from LMS_Mongodb_App.models import *
from datetime import datetime, timedelta
from django.db.models import Max, F ,Sum,Min,Count
# from django.contrib.postgres.aggregates import ArrayAgg
import json
from django.db.models.functions import TruncDate
from LMS_Project.Blobstorage import *
from .AppUsage import update_app_usage
from django.core.cache import cache
ONTIME = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
CONTAINER ="internship"
@api_view(['GET'])   
def home(request):
    return JsonResponse({"message": "Successfully Deployed on Azure at "+ str(ONTIME)},safe=False,status=200)

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
        update_app_usage(student_id)
        return JsonResponse(responce,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)    
def calculate_progress(start_date, end_date, student_progress,Total_days):
    days = student_progress.get('day')
    std_progress = int(days /int(Total_days) * 100)
    response = {
        "student_progress": std_progress if std_progress <= 100 else 100
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
        update_app_usage(student_id)
        return JsonResponse(responce,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
    
@api_view(['GET'])
def fetch_upcoming_events(request,Course_id):
    try:
        print(Course_id)
        current_time = datetime.utcnow() + timedelta(days=0,hours=5, minutes=30)
        blob_data = json.loads(get_blob('LMS_DayWise/Course0001.json'))
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
######################
@api_view(['GET'])
def get_weekly_progress(request,student_id):
    try:
        # obj = students_info.objects.get( student_id = student_id,del_row = False)
        assessment_data = students_assessments.objects.using('mongodb').filter(
            student_id = student_id,
            del_row = "False"
            ).order_by('-assessment_week_number').values_list('assessment_week_number','assessment_score_secured','assessment_max_score')
        practice_data = practice_questions.objects.using('mongodb').filter(
            student_id = student_id,
            del_row = "False"
            ).order_by('-practice_week_number').values_list('practice_week_number','practice_score_secured','practice_max_score')
        return JsonResponse({
            "assessment":list(assessment_data),
            "practice":list(practice_data),
                })
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
######################
@api_view(['GET'])
def fetch_study_hours_old(request,student_id,week):
    try:
        week = int(week)
        student = students_info.objects.get(student_id = student_id,del_row = False)
        course_subjects_data = course_subjects.objects.filter(course_id = student.course_id,del_row = False
                                                              ).values('subject_id__subject_name','duration_in_days','start_date','end_date')
        subjects ={}
        currentweek = {}
        for subject in course_subjects_data:
            weeks = []
            initial_date = subject.get('start_date')
            final_date = subject.get('end_date')
            today = timezone.now() + timedelta(days=7,hours=5, minutes=30)
            if  final_date < today or today < initial_date :
                break
            i = 1
            while initial_date <= final_date:
                week_start = initial_date - timedelta(days=initial_date.weekday())
                week_end = week_start + timedelta(days=6)  
                weeks.append({
                    'start': week_start.date(),
                    'end': week_end.date()
                })
                if timezone.is_naive(today):
                    today = timezone.make_aware(today, timezone.get_current_timezone())
                if week_start <= today<= week_end:
                    currentweek.update({subject.get('subject_id__subject_name'):i})
                    break
                i += 1
                initial_date = week_end + timedelta(days=1)
            subjects.update({subject.get('subject_id__subject_name'):weeks})
        subjects = subjects.get(list(currentweek.keys())[0])[currentweek.get(list(currentweek.keys())[0]) - 1]
        student_app_usages = student_app_usage.objects.filter(student_id = student_id,
                                                              logged_in__gte = subjects.get('start'),
                                                              logged_in__lte = subjects.get('end')+timedelta(days=1),
                                                              del_row = False
                ).annotate(date=TruncDate('logged_in')).values('date').annotate(
                total_study_hours=Sum(F('logged_out') - F('logged_in'))).order_by('date')
        response = {'daily_limit':2.0,
                    'weekly_limit':currentweek.get(list(currentweek.keys())[0]),
                    'hours':[]}
        hour_spent ={ i.get('date'):i.get('total_study_hours') for i in student_app_usages}
        for i in range(7):
            response.get('hours').append({
                "date":subjects.get('start') + timedelta(days=i),
                "day_name":calendar.day_name[(subjects.get('start') + timedelta(days=i)).weekday()][0:3],
                "isUpcoming":True if subjects.get('start') + timedelta(days=i) > datetime.utcnow().__add__(timedelta(hours=5,minutes=30)).date() else False,
                "isCurrent":True if subjects.get('start') + timedelta(days=i) == datetime.utcnow().__add__(timedelta(hours=5,minutes=30)).date() else False,
                "hours":round(hour_spent.get(subjects.get('start') + timedelta(days=i)).total_seconds()/3600,2) if hour_spent.get(subjects.get('start') + timedelta(days=i)) else 0
            })
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)


@api_view(['GET'])
def fetch_study_hours(request,student_id,week):
    try:
        student = students_info.objects.get(student_id = student_id,del_row = False)
        today =datetime.utcnow().__add__(timedelta(days=0,hours=5,minutes=30))
        if timezone.is_naive(today):
            today = timezone.make_aware(today, timezone.get_current_timezone())
        if week.isdigit():
            current_week = int(week)
        else:
            current_week = course_plan_details.objects.get(course_id = student.course_id,
                                                            day_date__date=today.date(),
                                                            del_row =False)
            if current_week is None:
                current_week =1,
            else:
                current_week=current_week.week
        course_details = list(course_plan_details.objects.filter(course_id=student.course_id,
                                                            week=current_week).values('duration_in_hours','day_date'))
        student_app_usages = student_app_usage.objects.filter(student_id = student_id,
                                                              logged_in__gte = course_details[0].get('day_date'),
                                                              logged_in__lte = course_details[-1].get('day_date')+timedelta(days=1),
                                                              del_row = False
                                                            ).annotate(date=TruncDate('logged_in')).values('date').annotate(
                                                            total_study_hours=Sum(F('logged_out') - F('logged_in'))).order_by('date')
        list_of_duration = [i.get("duration_in_hours")  for i in  course_details]
        response = {'daily_limit':sum(list_of_duration)/len(list_of_duration) if list_of_duration else 0,
                    'weekly_limit':current_week,
                    'hours':[]}
        hour_spent ={ i.get('date'):i.get('total_study_hours') for i in student_app_usages}
        for i in range(7):
            response.get('hours').append({
                "date":course_details[0].get('day_date') + timedelta(days=i),
                "day_name":calendar.day_name[(course_details[0].get('day_date') + timedelta(days=i)).weekday()][0:3],
                "isUpcoming":True if (course_details[0].get('day_date') + timedelta(days=i)).date() > today.date() else False,
                "isCurrent":True if (course_details[0].get('day_date') + timedelta(days=i)).date() == today.date() else False,
                "hours":round(hour_spent.get((course_details[0].get('day_date') + timedelta(days=i)).date()).total_seconds()/3600,2) if hour_spent.get((course_details[0].get('day_date') + timedelta(days=i)).date()) else 0
            })
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
        
@api_view(['GET'])
def fetch_calendar(request,student_id):
    try:
        current_time = datetime.utcnow() + timedelta(days=0,hours=5, minutes=30)
        blob_data = json.loads(get_blob('LMS_DayWise/Course0001.json'))
        student = students_info.objects.get(student_id = student_id,del_row = False)
        response = extract_calendar_events(blob_data,current_time)
        return JsonResponse({'year':(current_time.strftime("%Y")),
                              'month':str(int(current_time.strftime("%m"))-1),
                              "calendar":response},
                              safe=False,status=200)    
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
def extract_calendar_events(blob_data,current_time):
    events = []
    for event in blob_data:
        for i in blob_data.get(event):
            if i.get('topic') == 'Weekly Test' or i.get('topic') == 'Onsite Workshop' or i.get('topic') == 'Internship':
                date = datetime.strptime(str(i.get('date').replace('T',' ')).split('.')[0], "%Y-%m-%d %H:%M:%S") if str(i.get('date')).__contains__('T') else datetime.strptime(str(i.get('date')+" 00:00:00").split('.')[0], "%Y-%m-%d %H:%M:%S")
                events.append({
                    "title":i.get('topic'),
                    'subject':event,
                    "date":getdays(date)+" "+date.strftime("%Y"),
                    "time":date.strftime("%I:%M") + " " + date.strftime("%p"),
                    'datetime':date.date()
                })
    events = sorted(events, key=lambda k: k['datetime'])
    this_month = [event for event in events if calendar.month_abbr[int(event['datetime'].strftime("%m"))]==calendar.month_abbr[int(current_time.strftime("%m"))]]
    return this_month
@api_view(['GET'])
def fetch_student_summary(request,student_id):
    try:
        student = students_info.objects.get(student_id = student_id,del_row = False)
        student_app_usages = student_app_usage.objects.filter(student_id = student_id,
                                                              del_row = False
                                                            ).aggregate(
                                                            total_seconds=Sum(F('logged_out') - F('logged_in')))
        print(student_app_usages.get('total_seconds'))
        response ={
            'student_id': student.student_id,
            'name': student.student_firstname+' '+student.student_lastname,
            'score':student.student_score,
            'hour_spent':round(student_app_usages.get('total_seconds').total_seconds()/3600,2),
            'category':student.student_catogory,
            'college_rank':student.student_college_rank,
            'overall_rank':student.student_overall_rank

        }
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)        
@api_view(['GET'])
def fetch_top_navigation(request,student_id):
    try:
        notifications = list(notification.objects.using('mongodb').filter(
                                                                     student_id = student_id,
                                                                     status = 'U',
                                                                     del_row = False
                                                                     ).order_by('-notification_timestamp'
                                                                                ).values('notification_id','notification_title','notification_timestamp'))
        response = {
            'student_id': student_id,
            'count': len(notifications),
            'notifications': notifications
        }
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
    
# [
#     {
#       weekNumber: 1,
#       startDate: "19th Dec 24",
#       endDate: "25th Dec 24",
#       totalHours: "14hrs",
#       days: [
#         {
#           day: 1,
#           date: "19th Dec 24",
#           topics: ["Introduction", "Types and Query", "Select Query"],
#           practiceMCQ: { questions: "5/10", score: "3/10" },
#           practiceCoding: { questions: "5/10", score: "3/10" },
#           status: "Completed",
#         },
#         {
#           day: 2,
#           date: "20th Dec 24",
#           topics: ["Introduction to topic1", "Topic1", "Update Query"],
#           practiceMCQ: { questions: "5/10", score: "4/10" },
#           practiceCoding: { questions: "6/10", score: "4/10" },
#           status: "Completed",
#         },
#         {
#           day: 3,
#           date: "21st Dec 24",
#           topics: ["Advanced Queries", "Subqueries", "Group By"],
#           practiceMCQ: { questions: "5/10", score: "3/10" },
#           practiceCoding: { questions: "5/10", score: "3/10" },
#           status: "Completed",
#         },
#         {
#           day: 4,
#           date: "22nd Dec 24",
#           topics: ["Join ", "Indexing", "Normalization"],
#           practiceMCQ: { questions: "5/10", score: "4/10" },
#           practiceCoding: { questions: "5/10", score: "4/10" },
#           status: "Resume",
#         },
#         {
#           day: 5,
#           date: "24th Dec 24",
#           topics: ["Inner Join", "outer join", "cross join"],
#           practiceMCQ: { questions: "5/10", score: "4/10" },
#           practiceCoding: { questions: "5/10", score: "3/10" },
#           status: "Start",
#         },
#         {
#           day: 6,
#           date: "23rd Dec 24",
#           practiceMCQ: { questions: "5/10", score: "3/10" },
#           practiceCoding: { questions: "5/10", score: "3/10" },
#           status: "",
#           title: "Study day",
#         },
#         {
#           day: 7,
#           date: "25th Dec 24",
#           title: "Weekly Test",
#           testScore: { score: "90/100" },
#           status: "",
#         },
#       ],
#     },
#     {
#       weekNumber: 2,
#       startDate: "26th Dec 24",
#       endDate: "1st Jan 25",
#       totalHours: "14hrs",
#       days: [
#         {
#           day: 1,
#           date: "26th Dec 24",
#           topics: ["Advanced Queries", "Subqueries", "Group By"],
#           practiceMCQ: { questions: "6/10", score: "4/10" },
#           practiceCoding: { questions: "6/10", score: "4/10" },
#           status: "",
#         },
#         {
#           day: 2,
#           date: "27th Dec 24",
#           topics: ["Advanced Queries", "Subqueries", "Group By"],
#           practiceMCQ: { questions: "6/10", score: "5/10" },
#           practiceCoding: { questions: "6/10", score: "5/10" },
#           status: "",
#         },
#         {
#           day: 3,
#           date: "28th Dec 24",
#           topics: ["Join ", "Indexing", "Normalization"],
#           practiceMCQ: { questions: "6/10", score: "5/10" },
#           practiceCoding: { questions: "6/10", score: "4/10" },
#           status: "",
#         },
#         {
#           day: 4,
#           date: "29th Dec 24",
#           topics: ["Inner Join", "outer join", "cross join"],
#           practiceMCQ: { questions: "6/10", score: "5/10" },
#           practiceCoding: { questions: "6/10", score: "4/10" },
#           status: "",
#         },
#         {
#           day: 5,
#           date: "30th Dec 24",
#           topics: ["Advanced Queries", "Subqueries", "Full join"],
#           practiceMCQ: { questions: "6/10", score: "4/10" },
#           practiceCoding: { questions: "6/10", score: "5/10" },
#           status: "",
#         },
#         {
#           day: 6,
#           date: "31st Dec 24",
#           topics: ["Join Operations", "Indexing", "Normalization"],
#           practiceMCQ: { questions: "6/10", score: "5/10" },
#           practiceCoding: { questions: "6/10", score: "5/10" },
#           status: "",
#         },
#         {
#           day: 7,
#           date: "1st Jan 25",
#           testScore: { score: "85/100" },
#           status: "",
#         },
#       ],
#     },
#     {
#       weekNumber: 3,
#       startDate: "2nd Jan 25",
#       endDate: "8th Jan 25",
#       totalHours: "14hrs",
#       days: [
#         {
#           day: 1,
#           date: "2nd Jan 25",
#           topics: ["Triggers", "Stored Procedures", "Functions"],
#           practiceMCQ: { questions: "7/10", score: "6/10" },
#           practiceCoding: { questions: "7/10", score: "6/10" },
#           status: "",
#         },
#         {
#           day: 2,
#           date: "3rd Jan 25",
#           topics: ["Triggers", "Stored Procedures", "Functions"],
#           practiceMCQ: { questions: "7/10", score: "6/10" },
#           practiceCoding: { questions: "7/10", score: "6/10" },
#           status: "",
#         },
#         {
#           day: 3,
#           date: "4th Jan 25",
#           topics: ["Triggers", "Stored Procedures", "Functions"],
#           practiceMCQ: { questions: "7/10", score: "6/10" },
#           practiceCoding: { questions: "7/10", score: "5/10" },
#           status: "",
#         },
#         {
#           day: 4,
#           date: "5th Jan 25",
#           topics: ["Data Integrity", "Constraints", "Foreign Keys"],
#           practiceMCQ: { questions: "7/10", score: "6/10" },
#           practiceCoding: { questions: "7/10", score: "6/10" },
#           status: "",
#         },
#         {
#           day: 5,
#           date: "6th Jan 25",
#           topics: ["Data Integrity", "Constraints", "Foreign Keys"],
#           practiceMCQ: { questions: "7/10", score: "6/10" },
#           practiceCoding: { questions: "7/10", score: "5/10" },
#           status: "",
#         },
#         {
#           day: 6,
#           date: "7th Jan 25",
#           topics: ["Triggers", "Stored Procedures", "Functions"],
#           practiceMCQ: { questions: "7/10", score: "7/10" },
#           practiceCoding: { questions: "7/10", score: "6/10" },
#           status: "",
#         },
#         {
#           day: 7,
#           date: "8th Jan 25",
#           testScore: { score: "88/100" },
#           status: "",
#         },
#       ],
#     },
#     {
#       weekNumber: 4,
#       startDate: "9th Jan 25",
#       endDate: "15th Jan 25",
#       totalHours: "14hrs",
#       days: [
#         {
#           day: 1,
#           date: "9th Jan 25",
#           topics: ["Database Design", "Normalization", "ER Models"],
#           practiceMCQ: { questions: "8/10", score: "7/10" },
#           practiceCoding: { questions: "8/10", score: "7/10" },
#           status: "",
#         },
#         {
#           day: 2,
#           date: "10th Jan 25",
#           topics: ["Database Design", "Normalization", "ER Models"],
#           practiceMCQ: { questions: "8/10", score: "7/10" },
#           practiceCoding: { questions: "8/10", score: "7/10" },
#           status: "",
#         },
#         {
#           day: 3,
#           date: "11th Jan 25",
#           topics: ["Database Design", "Normalization", "ER Models"],
#           practiceMCQ: { questions: "8/10", score: "7/10" },
#           practiceCoding: { questions: "8/10", score: "7/10" },
#           status: "",
#         },
#         {
#           day: 4,
#           date: "12th Jan 25",
#           topics: ["Advanced SQL", "Optimization", "Indexing"],
#           practiceMCQ: { questions: "8/10", score: "7/10" },
#           practiceCoding: { questions: "8/10", score: "7/10" },
#           status: "",
#         },
#         {
#           day: 5,
#           date: "13th Jan 25",
#           topics: ["Advanced SQL", "Optimization", "Indexing"],
#           practiceMCQ: { questions: "8/10", score: "7/10" },
#           practiceCoding: { questions: "8/10", score: "7/10" },
#           status: "",
#         },
#         {
#           day: 6,
#           date: "14th Jan 25",
#           topics: ["Advanced SQL", "Optimization", "Indexing"],
#           practiceMCQ: { questions: "8/10", score: "7/10" },
#           practiceCoding: { questions: "8/10", score: "7/10" },
#           status: "",
#         },
#         {
#           day: 7,
#           date: "15th Jan 25",
#           testScore: { score: "92/100" },
#           status: "",
#         },
#       ],
#     },
#     {
#       weekNumber: 5,
#       startDate: "8th Jan 24",
#       endDate: "12th Jan 24",
#       title: "Workshop",
#     },
#     {
#       weekNumber: 6,
#       startDate: "8th Jan 24",
#       endDate: "12th Jan 24",
#       title: "Final Test",
#       Score: "150/200",
#       days: [
#         {
#           day: 1,
#           date: "8th Jan 24",
#           Questions: "25",
#           Coding: { questions: "5/25", score: "5/10" },
#           status: "",
#         },
#         {
#           day: 2,
#           date: "9th Jan 24",
#           Questions: "5",
#           Coding: { questions: "5/5", score: "8/10" },
#           status: "",
#         },
#         {
#           day: 3,
#           date: "10th Jan 24",
#           Questions: "10",
#           Coding: { questions: "5/10", score: "5/10" },
#           status: "",
#         },
#       ],
#     },
#     {
#       weekNumber: 7,
#       startDate: "8th Jan 24",
#       endDate: "12th Jan 24",
#       title: "Internship",
#       Score: "150/200",
#       days: [
#         {
#           day: 1,
#           date: "8th Jan 24",
#           Questions: "25",
#           Coding: { questions: "5/25", score: "5/10" },
#           status: "",
#         },
#         {
#           day: 2,
#           date: "9th Jan 24",
#           Questions: "5",
#           Coding: { questions: "5/5", score: "8/10" },
#           status: "",
#         },
#         {
#           day: 3,
#           date: "10th Jan 24",
#           Questions: "10",
#           Coding: { questions: "5/10", score: "5/10" },
#           status: "",
#         },
#       ],
#     },
#   ]
@api_view(['GET'])
def fetch_roadmap(request,student_id,course_id):
    try:
        blob_data = json.loads(get_blob('LMS_DayWise/Course0001.json'))
        course = courses.objects.get(course_id=course_id)
        sub = subjects.objects.get(subject_id = 'Subject4',del_row = False)
        course_details = list(course_plan_details.objects.filter(course_id=course, subject_id=sub, del_row=False)
                  .values('week')
                  .annotate(#   day_date_count=Count('day_date'), 
                      startDate=Min('day_date'),
                      endDate=Max('day_date'),
                      totalHours=Sum('duration_in_hours'),
                  )
                  .order_by('week'))
        student_question_details = students_details.objects.using('mongodb').get(
            student_id = student_id,del_row = 'False',
            # defaults = {
            #     'student_id': student_id,
            # }
        )
        sub_data = student_question_details.student_question_details.get(sub.subject_name)
        days = []
        other_weeks = []
        daynumber=0
        for i in course_details:
            week_data = sub_data.get('week_'+str(i.get('week')),{})

            for d in blob_data.get(sub.subject_name): 
                the_date = datetime.strptime(d.get('date').replace('T',' ').split('.')[0].replace('Z',''), "%Y-%m-%d %H:%M:%S")
                if i.get('startDate').date() <= the_date.date() and the_date.date() <= i.get('endDate').date():
                    day_data = week_data.get('day_'+str(d.get('day').split(' ')[-1]),{})
                    status = ''
                    mcq_qns =len(day_data.get('mcq_questions',[]))
                    coding_qns =  len(day_data.get('coding_questions',[]))
                    mcq_answered = len([dd for dd in day_data.get('mcq_questions_status',{}) if day_data.get('mcq_questions_status',{}).get(dd)==2])
                    coding_answered = len([dd for dd in day_data.get('coding_questions_status',{}) if day_data.get('coding_questions_status',{}).get(dd)==2])
                    if mcq_qns == mcq_answered and coding_qns == coding_answered and mcq_qns > 0 and coding_qns > 0:
                        status = 'Completed'
                    elif mcq_answered > 0 or coding_answered > 0 or day_data != {}:
                        status = 'Resume'
                    else:
                        prev_day_data = week_data.get('day_'+str(daynumber),{})
                        prev_mcq_qns =len(prev_day_data.get('mcq_questions',[]))
                        prev_coding_qns =  len(prev_day_data.get('coding_questions',[]))
                        prev_mcq_answered = len([dd for dd in prev_day_data.get('mcq_questions_status',{}) if prev_day_data.get('mcq_questions_status',{}).get(dd)==2])
                        prev_coding_answered = len([dd for dd in prev_day_data.get('coding_questions_status',{}) if prev_day_data.get('coding_questions_status',{}).get(dd)==2])
                        if prev_mcq_qns == prev_mcq_answered and prev_coding_qns == prev_coding_answered and prev_mcq_qns > 0 and prev_coding_qns > 0:
                            status = 'Start'
                    if d.get('topic') == 'Weekly Test':# or d.get('topic') == 'Onsite Workshop' or d.get('topic') == 'Internship':
                        days.append({'day':daynumber+1,'day_key':d.get('day').split(' ')[-1],
                            "date":getdays(the_date)+" "+the_date.strftime("%Y")[2:],
                            'week':i.get('week'),
                            'topics':d.get('topic'),
                            'score' :'0/0',

                            'status':status
                              })
                    elif d.get('topic') == 'Onsite Workshop' or d.get('topic') == 'Final Test':
                        other_weeks.append({#'day':daynumber+1,
                            'day_key':d.get('day').split(' ')[-1],
                            "date":getdays(the_date)+" "+the_date.strftime("%Y")[2:],
                            'week':len(course_details)+other_weeks.__len__()+1,
                            'topics':d.get('topic'),
                            'score' :'0/0',
                            'days':[],
                            'status':''
                              })
                    elif d.get('topic') == 'Internship':
                        other_weeks.append({'day':'',
                            'day_key':d.get('day').split(' ')[-1],
                            "date":getdays(the_date)+" "+the_date.strftime("%Y")[2:],
                            'week':len(course_details)+other_weeks.__len__()+1,
                            'topics':d.get('topic'),
                            'score' :'0/0',
                            'days':[],
                            'status':''
                              })
                    else:
                        days.append({'day':daynumber+1,'day_key':d.get('day').split(' ')[-1],
                            "date":getdays(the_date)+" "+the_date.strftime("%Y")[2:],
                            'week':i.get('week'),
                            'topics':d.get('topic'),
                            'practiceMCQ': { 'questions': str(mcq_answered)
                                            +'/'+str(mcq_qns),
                                             'score': day_data.get('mcq_score','0/0') },
                            'practiceCoding': { 'questions': str(coding_answered)
                                            +'/'+str(coding_qns),
                                             'score': day_data.get('coding_score','0/0') },
                            'status':status
                              })
                    daynumber+=1    
            i.update({'days': days})
            days = []
        course_details.extend(other_weeks)
        response = {
            "weeks":course_details,
        }
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)

@api_view(['GET'])
def fetch_learning_modules(request,student_id,subject,day_number):
    try:
        student = students_info.objects.get(student_id = student_id,del_row = False)
        blob_data = json.loads(get_blob('LMS_DayWise/'+student.course_id.course_id+'.json'))
        response = [day  for day in blob_data.get(subject) if day.get('day') == 'Day '+str(day_number)][0].get('content')
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
@api_view(['POST'])
def add_days_to_student(request):
    try:
        data = json.loads(request.body)
        student = students_details.objects.using('mongodb').get(student_id = data.get('student_id'),
                                                                del_row = 'False')
        needTOsave = False
        if student.student_question_details.get(data.get('subject')) == None:
            student.student_question_details.update({
                data.get('subject'):{
                    'week_'+str(data.get('week_number')):{}
            }})
            needTOsave = True
        if student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))) == None:
            student.student_question_details.get(data.get('subject')).update({
                'week_'+str(data.get('week_number')):{
                        'day_'+str(data.get('day_number')):{}
                    }
            })
            needTOsave = True
        if student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))) == None:
            student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).update({
                'day_'+str(data.get('day_number')):{}
            })
            needTOsave = True
        response = {'message':'not updated'}
        if needTOsave == True :
            student_info = students_info.objects.get(student_id = data.get('student_id'),del_row = False)
            blob_data = json.loads(get_blob('LMS_DayWise/'+student_info.course_id.course_id+'.json'))
            day_data = [day  for day in blob_data.get(data.get('subject')) if day.get('day') == 'Day '+str(data.get('day_number'))][0]
            types = []
            levels ={}
            if day_data.get('mcq'):
                types.append('MCQ')
                levels.update({'MCQ':day_data.get('mcq')})
            if day_data.get('coding'):
                types.append('Coding')
                levels.update({'Coding':day_data.get('coding')})
            qnslist = get_random_questions(types,day_data.get('subtopicid'),levels)
            student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))).update({
                "mcq_questions": qnslist.get('MCQ'),
                "mcq_questions_status": {i:0 for i in qnslist.get('MCQ')},
                "mcq_score": "0/"+str(qnslist.get('MCQ_score')),
                "coding_questions": qnslist.get('Coding'),
                "coding_questions_status": {i:0 for i in qnslist.get('Coding')},
                "coding_score": "0/"+str(qnslist.get('Coding_score'))
            })
            student.save()
            response.update({'message':'updated'})
        
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
@api_view(['GET'])
def fetch_overview_modules(request,student_id,subject,day_number):
    try:
        student = students_info.objects.get(student_id = student_id,del_row = False)
        blob_data = json.loads(get_blob('LMS_DayWise/'+student.course_id.course_id+'.json'))
        response = [day  for day in blob_data.get(subject) if day.get('day') == 'Day '+str(day_number)]
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
    
@api_view(['GET'])
def fetch_questions(request,type,student_id,subject,day_number,week_number):
    try:
        student = students_details.objects.using('mongodb').get(student_id = student_id,del_row = 'False')
        if student.student_question_details.get(subject) == None:
            return JsonResponse({"message": "subject not found"},safe=False,status=400)
        if student.student_question_details.get(subject).get('week_'+week_number) == None:
            return JsonResponse({"message": "week not found"},safe=False,status=400)
        if student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number) == None:
            return JsonResponse({"message": "day not found"},safe=False,status=400)
        questions_ids = (student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number).get('mcq_questions' if type.lower() =='mcq' else 'coding_questions'))
        qn_data = get_list_blob('LMSData/',questions_ids,type.upper() if type.lower() =='mcq' else type[0].upper()+str(type[1:]).lower()  )
        return JsonResponse(qn_data,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
@api_view(['POST'])
def submit_MCQ_Question(request):
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        question_id = data.get('question_id')
        student_practiceMCQ_answer ,created= student_practiceMCQ_answers.objects.using('mongodb'
                                                            ).get_or_create(student_id = student_id,
                                                                 question_id = question_id,
                                                                 del_row = 'False' ,
                                                                 defaults={
                                                                     'student_id':student_id,
                                                                     'question_id':question_id,
                                                                    'correct_ans': data.get('correct_ans'),
                                                                    'entered_ans': data.get('entered_ans'),
                                                                    'subject_id':data.get('subject_id'),
                                                                    'answered_time':timezone.now() + timedelta(hours=5, minutes=30)
                                                                 })
        response ={'message':'Already Submited'}
        if created:
            blob_rulea_data = json.loads(get_blob('LMS_Rules/Rules.json')).get('mcq')
            student = students_details.objects.using('mongodb').get(student_id = student_id,
                                                                    del_row = 'False')
            print(blob_rulea_data)
            score = 0
            if data.get('correct_ans') == data.get('entered_ans'):
                if question_id[-4]=='e':
                    score = [i.get('score') for i in blob_rulea_data if i.get('level') == 'level1'.get('level')][0]
                elif question_id[-4]=='m':
                    score = [i.get('score') for i in blob_rulea_data if i.get('level') == 'level2'.get('level')][0]
                elif question_id[-4]=='h':
                    score = [i.get('score') for i in blob_rulea_data if i.get('level') == 'level3'.get('level')][0]
            old_score = student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))).get('mcq_score').split('/')
            score = str(int(old_score[0]) + score) + '/' + str(int(old_score[1]))
            student.student_question_details.get(data.get('subject')
                                                 ).get('week_'+str(data.get('week_number'))
                                                       ).get('day_'+str(data.get('day_number'))
                                                             ).get('mcq_questions_status'
                                                                   ).update({question_id:2,
                                                                             'mcq_score':score})
            response ={'message':student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number')))}
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed"},safe=False,status=400)
