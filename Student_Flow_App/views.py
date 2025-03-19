import calendar
from itertools import count
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from LMS_MSSQLdb_App.models import *
from LMS_Mongodb_App.models import *
from datetime import datetime, timedelta
from django.utils import timezone
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
    return JsonResponse({"message": "Successfully Deployed LMS on Azure at "+ str(ONTIME)},safe=False,status=200)

@api_view(['GET'])
def fetch_enrolled_subjects(request,student_id):
    try:
        student_data = students_info.objects.get(student_id = student_id,del_row = False)
        enrolled_subjects = course_subjects.objects.filter(course_id = student_data.course_id,del_row = False)
        latest_activities = student_activities.objects.filter(student_id=student_id,del_row=False).values('subject_id__subject_name').annotate(latest_day=Max('activity_day'))
        sub_days_count = {}
        [sub_days_count.update({activity['subject_id__subject_name']:{'day':activity['latest_day']}})for activity in latest_activities]
        # print(sub_days_count)
        response = []
        for subject in enrolled_subjects:
            subject_data = {}
            subject_data.update({
                "title": subject.subject_id.subject_name,
                "image": subject.path,
                "duration": f"{getdays(subject.start_date)} - {getdays(subject.end_date)}",
                "progress": calculate_progress(subject.start_date,subject.end_date,sub_days_count.get(subject.subject_id.subject_name,{'day':0}),subject.duration_in_days),
            })
            response.append(subject_data)
        update_app_usage(student_id)
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)    
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
       formatted_date =  (f"{day}{suffix} {calendar.month_abbr[month]} {date.strftime('%Y')[2:]}")
       return formatted_date


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
        response = [{
            "title":session[0],
            "date":getdays(session[1])+" "+session[1].strftime("%Y")[2:],
            "time":session[1].strftime("%I:%M") + " " + session[1].strftime("%p")}            for session in live_session ]
        update_app_usage(student_id)
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
    
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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
    
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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)


@api_view(['GET'])
def fetch_study_hours(request,student_id,week):
    try:
        student = students_info.objects.get(student_id = student_id,del_row = False)
        today =timezone.now() + timedelta(hours=5, minutes=30)
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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
        
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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)        
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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
    

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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)

@api_view(['GET'])
def fetch_learning_modules(request,student_id,subject,day_number):
    try:
        student = students_info.objects.get(student_id = student_id,del_row = False)
        blob_data = json.loads(get_blob('LMS_DayWise/'+student.course_id.course_id+'.json'))
        day_data = [day  for day in blob_data.get(subject) if day.get('day') == 'Day '+str(day_number)][0] 
        response_data =[]
        for i in day_data.get('subtopicids'):
            response_data.append({
                'subtopicid':i.get('subtopic_id'),
                'sub_topic':i.get('subtopic_name'),
                'lesson': [subdata.get('path') for subdata in day_data.get('content').get(i.get('subtopic_id')) if subdata.get('type')=="video"],
                'notes': [subdata.get('path') for subdata in day_data.get('content').get(i.get('subtopic_id')) if subdata.get('type')=="file"],
                'mcqQuestions':sum([ day_data.get('mcq').get(i.get('subtopic_id')).get(qn) for qn in day_data.get('mcq').get(i.get('subtopic_id')) ]),
                'codingQuestions':sum([day_data.get('coding').get(i.get('subtopic_id')).get(qn) for qn in day_data.get('coding').get(i.get('subtopic_id') )])
            })
        response =  [
        {
            'Day': day_data.get('day'),
            'title':  day_data.get('topic'),
            'duration':  day_data.get('duration'),
            'sub_topic_data':response_data
        }]
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
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
            cache_data = cache.get('LMS_DayWise/'+student_info.course_id.course_id+'.json')
            if cache_data :
                cache.set('LMS_DayWise/'+student_info.course_id.course_id+'.json',cache_data)
                blob_data = cache_data
            else:
                blob_data = json.loads(get_blob('LMS_DayWise/'+student_info.course_id.course_id+'.json'))
                cache.set('LMS_DayWise/'+student_info.course_id.course_id+'.json',blob_data)
            day_data = [day  for day in blob_data.get(data.get('subject')) if day.get('day') == 'Day '+str(data.get('day_number'))][0]
            types = []
            levels ={}
            if day_data.get('mcq'):
                types.append('MCQ')
                levels.update({'MCQ':day_data.get('mcq')})
            if day_data.get('coding'):
                types.append('Coding')
                levels.update({'Coding':day_data.get('coding')})
            qnslist = get_random_questions(types,[st.get('subtopic_id') for st in day_data.get('subtopicids')],levels)
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
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
@api_view(['GET'])
def fetch_overview_modules(request,student_id,subject,day_number):
    try:
        student = students_info.objects.get(student_id = student_id,del_row = False)
        blob_data = json.loads(get_blob('LMS_DayWise/'+student.course_id.course_id+'.json'))
        response = [day  for day in blob_data.get(subject) if day.get('day') == 'Day '+str(day_number)]
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
# @api_view(['GET'])
# def fetch_questions_and_status(request,type,student_id,subject,day_number,week_number,subTopic):
#     try:
#         student = students_details.objects.using('mongodb').get(student_id = student_id,del_row = 'False')
#         if student.student_question_details.get(subject) == None:
#             return JsonResponse({"message": "subject not found"},safe=False,status=400)
#         if student.student_question_details.get(subject).get('week_'+week_number) == None:
#             return JsonResponse({"message": "week not found"},safe=False,status=400)
#         if student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number) == None:
#             return JsonResponse({"message": "day not found"},safe=False,status=400)
#         questions_ids = (student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number).get('mcq_questions' if type.lower() =='mcq' else 'coding_questions'))
#         if type .lower() == 'mcq':
#             student_answers = list(student_practiceMCQ_answers.objects.using('mongodb').filter(student_id = student_id,
#                                                                                           question_id__in = questions_ids,
#                                                                                             del_row = 'False').values('question_id','score'))
#         else:
#             student_answers = list(student_practice_coding_answers.objects.using('mongodb').filter(student_id = student_id,
#                                                                                                    subject_id = subject,
#                                                                                           question_id__in = questions_ids,
#                                                                                             del_row = 'False').values('question_id','score'))
#         student_answers = {ans.get('question_id'):ans.get('score') for ans in student_answers}
#         qn_data = get_questions_staus('LMSData/',[qn for qn in questions_ids if qn[1:-5] == subTopic],type.upper() if type.lower() =='mcq' else type[0].upper()+str(type[1:]).lower()  )
#         response = [qn.update({
#             'status': True if student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number).get(type.lower()+'_questions_status').get(qn.get('Qn_name')) == 2 else False
#             ,'score':str(student_answers.get(qn.get('Qn_name'),'0'))+'/'+qn.get('score')               }) for qn in qn_data ]
#         return JsonResponse(qn_data,safe=False,status=200)
#     except Exception as e:
#         print(e)
#         return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400) 
@api_view(['GET'])
def fetch_questions(request,type,student_id,subject,subject_id,day_number,week_number,subTopic):
    try:
        student = students_details.objects.using('mongodb').get(student_id = student_id,del_row = 'False')
        if student.student_question_details.get(subject) == None:
            return JsonResponse({"message": "subject not found"},safe=False,status=400)
        if student.student_question_details.get(subject).get('week_'+week_number) == None:
            return JsonResponse({"message": "week not found"},safe=False,status=400)
        if student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number) == None:
            return JsonResponse({"message": "day not found"},safe=False,status=400)
        questions_ids = (student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number).get('mcq_questions' if type.lower() =='mcq' else 'coding_questions'))
        if type .lower() == 'mcq':
            student_answers = list(student_practiceMCQ_answers.objects.using('mongodb').filter(student_id = student_id,
                                                                                                subject_id = subject_id,
                                                                                          question_id__in = questions_ids,
                                                                                            del_row = 'False').values('question_id','score'))
        else:
            student_answers = list(student_practice_coding_answers.objects.using('mongodb').filter(student_id = student_id,
                                                                                                   subject_id = subject_id,
                                                                                          question_id__in = questions_ids,
                                                                                            del_row = 'False').values('question_id','score'))
        student_answers = {
            ans.get('question_id'):ans.get('score') if int(str(ans.get('score')).split('.')[1]) > 0 else int(str(ans.get('score')).split('.')[0])
            for ans in student_answers}
        container_client =  get_blob_container_client()
        qn_data = []
        blob_path = 'LMSData/'
        list_of_qns = [qn for qn in questions_ids if qn[1:-5] == subTopic]
        cacheresponse = cache.get('LMS_Rules/Rules.json')
        if cacheresponse:
            # print('cache hit')
            cache.set('LMS_Rules/Rules.json',cacheresponse)
            Rules = cacheresponse
        else:
            blob_client = container_client.get_blob_client('LMS_Rules/Rules.json')
            Rules = json.loads(blob_client.download_blob().readall())
            cache.set('LMS_Rules/Rules.json',Rules)
        if type.lower() == 'mcq':
            for Qn in list_of_qns:
                path = f'{blob_path}{Qn[1:3]}/{Qn[1:-7]}/{Qn[1:-5]}/{type.upper()}/{Qn}.json'
                cacheres = cache.get(path)
                if cacheres:
                    # print('cache hit')
                    cache.set(path,cacheres)
                    blob_data = cacheres
                else:
                    blob_client = container_client.get_blob_client(path)
                    blob_data = json.loads(blob_client.download_blob().readall())
                    cache.set(path,blob_data)
                blob_data.update({'Qn_name':Qn,
                                  'score':str(student_answers.get(Qn,'0'))+'/'+Rules.get(type.lower(),[])[0].get('score'),
                                  'status': True if student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number).get(type.lower()+'_questions_status').get(Qn) == 2 else False
                                  })
                qn_data.append(blob_data)
        elif type.lower() == 'coding':
            for Qn in list_of_qns:
                path = f'{blob_path}{Qn[1:3]}/{Qn[1:-7]}/{Qn[1:-5]}/{type[0].upper()+str(type[1:]).lower()}/{Qn}.json'
                cacheres = cache.get(path)
                if cacheres:
                    # print('cache hit')
                    cache.set(path,cacheres)
                    blob_data = cacheres
                else:
                    blob_client = container_client.get_blob_client(path)
                    blob_data = json.loads(blob_client.download_blob().readall())
                    cache.set(path,blob_data)
                blob_data.update({'Qn_name':Qn,
                                  'score':str(student_answers.get(Qn,'0'))+'/'+Rules.get(type.lower(),[])[0].get('score'),
                                  'status': True if student.student_question_details.get(subject).get('week_'+week_number).get('day_'+day_number).get(type.lower()+'_questions_status').get(Qn) == 2 else False
                                  })
                qn_data.append(blob_data)
        container_client.close()
        return JsonResponse(qn_data,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)

@api_view(['POST'])
def submit_MCQ_Question(request):
    de_buging = ''
    try:
        de_buging = '-1 '
        data = json.loads(request.body)
        de_buging = de_buging + '0 '
        student_id = data.get('student_id')
        de_buging = de_buging + '0.1 '
        question_id = data.get('question_id')
        de_buging = de_buging + '0.2 '
        blob_rules_data = json.loads(get_blob('LMS_Rules/Rules.json'))
        de_bugging = de_bugging + '0.3 '
        blob_rules_data = blob_rules_data.get('mcq')
        de_buging = de_buging + '0.4 '
        score = 0
        de_buging = de_buging + '1 '
        if data.get('correct_ans') == data.get('entered_ans'):
                if question_id[-4]=='e':
                    score = [i.get('score') for i in blob_rules_data if i.get('level').lower() == 'level1'][0]
                elif question_id[-4]=='m':
                    score = [i.get('score') for i in blob_rules_data if i.get('level').lower() == 'level2'][0]
                elif question_id[-4]=='h':
                    score = [i.get('score') for i in blob_rules_data if i.get('level').lower() == 'level3'][0]
        de_buging = de_buging + '2 '
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
                                                                    'score':score,
                                                                    'answered_time':timezone.now() + timedelta(hours=5, minutes=30)
                                                                 })
        de_buging = de_buging + '3 '
        response ={'message':'Already Submited'}
        if created:
            student = students_details.objects.using('mongodb').get(student_id = student_id,
                                                                    del_row = 'False')
            de_buging = de_buging + '4 '
            student_info = students_info.objects.get(student_id = student_id,del_row = False)   
            de_buging = de_buging + '5 '
            if student.student_question_details.get(data.get('subject')) == None:
                student.student_question_details.update({
                    data.get('subject'):{
                        'week_'+str(data.get('week_number')):{}
                }})
            de_buging = de_buging + '6 '
            if student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))) == None:
                student.student_question_details.get(data.get('subject')).update({
                    'week_'+str(data.get('week_number')):{
                            'day_'+str(data.get('day_number')):{}
                        }
                })
            de_buging = de_buging + '7 '
            if student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))) == None:
                student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).update({
                    'day_'+str(data.get('day_number')):{
                            'mcq_questions_status':{},
                            'mcq_score':'0/0'
                    }
                })
            de_buging = de_buging + '8 '
            old_score = student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))).get('mcq_score','0/0').split('/')
            de_buging = de_buging + '9 '
            newscore = str(int(old_score[0]) + int(score)) + '/' + old_score[1]
            de_buging = de_buging + '10 '
            student.student_question_details.get(data.get('subject')
                                                 ).get('week_'+str(data.get('week_number'))
                                                       ).get('day_'+str(data.get('day_number'))
                                                             ).get('mcq_questions_status'
                                                                   ).update({question_id:2}) 
            de_buging = de_buging + '11 '           
            student.student_question_details.get(data.get('subject')
                                                 ).get('week_'+str(data.get('week_number'))
                                                       ).get('day_'+str(data.get('day_number'))
                                                             ).update({'mcq_score':newscore})
            de_buging = de_buging + '12 '
            student.save()
            de_buging = de_buging + '13 '
            student_info.student_score = int(student_info.student_score) + int(score)
            de_buging = de_buging + '14 '
            student_info.save()
            de_buging = de_buging + '15 '
            response ={'message':'Submited'}
        de_buging = de_buging + '16 '
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","de_buging":de_buging,"error":str(e)},safe=False,status=400)
@api_view(['PUT']) 
def submition_coding_question(request):
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        question_id = data.get('Qn')
        student = students_details.objects.using('mongodb').get(student_id = student_id,
                                                                del_row = 'False')
        # if student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))).get('coding_questions_status').get(question_id) ==2:
        #     return JsonResponse({ "message": "Already Submited",},safe=False,status=200)
        blob_rules_data = json.loads(get_blob('LMS_Rules/Rules.json')).get('coding')
        score = 0
        if data.get('correct_ans') == data.get('entered_ans'):
                if question_id[-4]=='e':
                    score = [i.get('score') for i in blob_rules_data if i.get('level').lower() == 'level1'][0]
                elif question_id[-4]=='m':
                    score = [i.get('score') for i in blob_rules_data if i.get('level').lower() == 'level2'][0]
                elif question_id[-4]=='h':
                    score = [i.get('score') for i in blob_rules_data if i.get('level').lower() == 'level3'][0]
        score = int(score)

        result = {}
        i = 0
        passedcases = 0
        totalcases = 0
        if data.get("subject") == 'HTML' or data.get("subject") == 'HTML CSS' or data.get("subject") == 'CSS' or data.get("subject") == 'Java Script':
                passedcases = float(str(data.get("final_score")).split('/')[0])
                totalcases = float(str(data.get("final_score")).split('/')[1])
                result = { 'TestCases':data.get("final_score")}
        else:
            for r in data.get('Result'):
                i += 1
                if r.get("TestCase" + str(i)) == 'Passed' or r.get("TestCase" + str(i)) == 'Failed':
                    totalcases += 1
                    if r.get("TestCase" + str(i)) == 'Passed':
                        passedcases += 1
                    result.update(r)
                if r.get("Result") == 'True' or r.get("Result") == 'False':
                    result.update(r)
            if passedcases == totalcases and passedcases ==0:
                score = 0
            
        score = round(score*(passedcases/totalcases),2)
        # print('SCore',score,'passedcases',passedcases,'totalcases',totalcases)
        user , created = student_practice_coding_answers.objects.using('mongodb').get_or_create(student_id=student_id,
                                                                                          subject_id=data.get('subject_id'),
                                                                                          question_id=question_id,
                                                                                          del_row='False',
                                                                                          defaults={
                                                                                              'student_id':data.get('student_id'),
                                                                                              'subject_id':data.get('subject_id'),
                                                                                              'question_id':question_id,
                                                                                              'entered_ans':data.get('Ans'),
                                                                                              'answered_time':timezone.now() + timedelta(hours=5, minutes=30),
                                                                                              'testcase_results':result,
                                                                                              'Attempts':1,
                                                                                              'score':score
                                                                                          })
        response ={'message':'Submited'}
        if created:
            response.update({'message':'Submited','new':'True'})
        else:
            user.entered_ans    = data.get('Ans')
            user.answered_time  = timezone.now() + timedelta(hours=5, minutes=30)
            user.testcase_results = result
            user.score = score
            user.save()
        
        student_info = students_info.objects.get(student_id = student_id,del_row = False)
        old_score = student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))).get('coding_score').split('/')
        newscore = str(int(old_score[0]) + int(score)) + '/' + old_score[1]
        student.student_question_details.get(data.get('subject')
                                             ).get('week_'+str(data.get('week_number'))
                                                   ).get('day_'+str(data.get('day_number'))
                                                         ).get('coding_questions_status'
                                                               ).update({question_id:2})   
        student.student_question_details.get(data.get('subject')
                                             ).get('week_'+str(data.get('week_number'))
                                                   ).get('day_'+str(data.get('day_number'))
                                                         ).update({'coding_score':newscore})
        student.save()
        student_info.student_score = int(student_info.student_score) + int(score)
        student_info.save()
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)

@api_view(['GET'])
def fetch_all_live_session(request,student_id):
    try:
        live_session = list(live_sessions.objects.using('mongodb').filter(student_ids__contains = student_id,
                                                                     del_row = "False"
                                                                     ).order_by('-session_starttime').values(
                                                                         'session_id',
                                                                         'session_title',
                                                                         'session_starttime',
                                                                         'session_meetlink',
                                                                         'session_video_link',
                                                                         'session_status',
                                                                         'session_endtime'
                                                                     ))
        if live_session == []:
            return JsonResponse({"message": "No Live Session"},safe=False,status=400)
        attendance = participant.objects.using('mongodb').filter(session_id__in = [session.get('session_id') for session in live_session],
                                                                     student_id = student_id,
                                                                     del_row = "False"
                                                                     ).order_by('-attended_time').values(
                                                                         'session_id',
                                                                         'student_id',
                                                                         'attended_time',
                                                                     )
        response = [{
                    'id':  session.get('session_id'),
                    'name': session.get('session_title'),
                    'date': session.get('session_starttime').strftime("%Y-%m-%d"),
                    'time': session.get('session_starttime').strftime("%I:%M") + " " + session.get('session_starttime').strftime("%p"),
                    'meet_link': session.get('session_meetlink'),
                    # 'duration': [duration.get('attended_time') for duration in attendance if duration.get('session_id'  ) == str(session.get('session_id'))][0],
                    # 'total_duration': (session.get('session_endtime')-session.get('session_starttime')).total_seconds(),
                    'attendance': '-/-'if session.get('session_status') != 'Completed' else round(([duration.get('attended_time'
                                                                                                                  ) for duration in attendance if duration.get('session_id'  
                                                                                                                                                               ) == str(session.get('session_id'))][0]/(session.get('session_endtime')-session.get('session_starttime')).total_seconds())*100,2),
                    'video_link': session.get('session_video_link'),
                    'ended': True if session.get('session_status') == 'Completed' else False,
                    'status':session.get('session_status')
                    }            for session in live_session ]
        return JsonResponse((response),safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
@api_view(['GET'])
def fetch_all_test_details(request,student_id):
    try:
        students_assessment = students_assessments.objects.using('mongodb'
                                                                 ).filter(student_id = student_id,
                                                                     del_row = False
                                                                     ).values(
                                                                         'assessment_type',
                                                                         'subject_id',
                                                                         'test_id',
                                                                         'course_id',
                                                                         'assessment_status',
                                                                         'assessment_score_secured',
                                                                         'assessment_max_score',
                                                                         'assessment_week_number',
                                                                         'assessment_completion_time'
                                                                     )
        if students_assessment == []:
            return JsonResponse({"message": "No Test Available"},safe=False,status=400)
        test_detail_obj = test_sections.objects.filter(test_id__test_id__in = [test.get('test_id') for test in students_assessment],
                                                  del_row = False) 
        test_detail = {test.test_id.test_id:test for test in test_detail_obj} 
        response =[{
            "test_type": test_detail.get(test.get('test_id')).test_id.test_type,
            "test_id":  test.get('test_id'),
            "test_status":  test.get('assessment_status'),
            "score": str(test.get('assessment_score_secured'))+'/'+str(test_detail.get(test.get('test_id')).test_id.test_marks),
            'topic':test_detail.get(test.get('test_id')).topic_id.topic_name,
            "subject":  test_detail.get(test.get('test_id')).test_id .subject_id.subject_name,
            "startdate": test_detail.get(test.get('test_id')).test_id .test_date_and_time.strftime("%Y-%m-%d"),
            "starttime":test_detail.get(test.get('test_id')).test_id .test_date_and_time.strftime("%I:%M") + " " + test_detail.get(test.get('test_id')).test_id .test_date_and_time.strftime("%p"),
            "enddate": test_detail.get(test.get('test_id')).test_id .test_date_and_time.strftime("%Y-%m-%d"),
            "endtime": (test_detail.get(test.get('test_id')).test_id .test_date_and_time.__add__(timedelta(minutes = int(test_detail.get(test.get('test_id')).test_id.test_duration)))).strftime("%I:%M") + " " + (test_detail.get(test.get('test_id')).test_id .test_date_and_time.__add__(timedelta(minutes = int(test_detail.get(test.get('test_id')).test_id.test_duration)))).strftime("%p"),
            "title":test_detail.get(test.get('test_id')).test_id .test_name,            
        }  for test in students_assessment]
        return JsonResponse({'test_details':response},safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)

@api_view(['POST'])
def submit_Tickets(request):
    try:
        data = json.loads(request.body)
        ticket = issue_details.objects.using('mongodb').create(
            student_id = data.get('student_id'),
            image_path = data.get('img_path'),
            issue_description = data.get('issue_description'),
            issue_status = data.get('issue_status','Pending'),
            issue_type = data.get('issue_type'),
            resolved_time = None,
            reported_time = timezone.now() + timedelta(hours=5, minutes=30),
        )
        
        return JsonResponse({"message": "Success"},safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
@api_view(['GET'])
def fetch_all_tickets(request,student_id):
    try:
        tickets = list(issue_details.objects.using('mongodb').filter(student_id = student_id,del_row = 'False').order_by('-reported_time').values())
        return JsonResponse({'ticket_details':tickets},safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
@api_view(['PUT'])
def student_side_comments_for_tickets(request):
    try:
        data = json.loads(request.body)
        ticket = issue_details.objects.using('mongodb').get(student_id = data.get('student_id'),sl_id = data.get('t_id'),del_row = 'False')
        keys = sorted([int(str(tk).replace('stu','')) for tk in ticket.comments if str(tk).startswith('stu')])
        print(keys[-1]+1 if len(keys)>0 else [0] )
        ticket.comments.update({
            "stu"+str(keys[-1]+1 if len(keys)>0 else 1): {
                    "role": "student",
                    "comment": data.get('comment'),
                    "timestamp": timezone.now() + timedelta(hours=5, minutes=30)
                    },})
        ticket.save()
        responnse=ticket.comments
        return JsonResponse({'message':responnse},safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
    
@api_view(['GET'])
def fetch_FAQ(request):
    try: 
        return JsonResponse(json.loads(get_blob('FAQ/faq.json')),safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)