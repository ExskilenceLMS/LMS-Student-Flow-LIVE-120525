import json
from django.test import TestCase

# # Create your tests here.
# from django.http import HttpResponse, JsonResponse
# from rest_framework.decorators import api_view
# from LMS_MSSQLdb_App.models import *
# from LMS_Mongodb_App.models import *
# from datetime import datetime, timedelta

# @api_view(['GET'])
# def addLiveSession(request):
#     try:

#         obj = live_sessions.objects.using('mongodb').create(
#             # session_id = 'Session1',
#             session_title = 'Week 1 Python Discussion',
#             session_starttime = datetime.utcnow().__add__(timedelta(days=1,hours=5,minutes=30)),
#             session_author = 'TEST',
#             session_subject = 'subject1',
#             session_meetlink = 'https://meet.google.com/bba-rfhf-hvk',
#             session_endtime = datetime.utcnow().__add__(timedelta(days=1,hours=6,minutes=30)),
#             session_video_link = 'https://www.youtube.com/watch?v=KUECJHlV1LE&t=332s&pp=ygUnZG93bmxvYWQgaW1hZ2UgZnJvbSBkb2NrZXIgdXNpbmcgcHl0aG9u',
#             session_status = 'UPCOMING',
#             del_row = 'False'
#         )
#         obj1 = live_sessions.objects.using('mongodb').create(
#             # session_id = 'Session2',
#             session_title = 'Week 2 Python Discussion',
#             session_starttime = datetime.utcnow().__add__(timedelta(days=1,hours=5,minutes=30)),
#             session_author = 'TEST',
#             session_subject = 'subject1',
#             session_meetlink = 'https://meet.google.com/bba-rfhf-hvk',
#             session_endtime = datetime.utcnow().__add__(timedelta(days=1,hours=6,minutes=30)),
#             session_video_link = 'https://www.youtube.com/watch?v=KUECJHlV1LE&t=332s&pp=ygUnZG93bmxvYWQgaW1hZ2UgZnJvbSBkb2NrZXIgdXNpbmcgcHl0aG9u',
#             session_status = 'UPCOMING',
#             student_ids = ['25MRITCS001'],
#             del_row = 'False'
#         )
#         obj2 = live_sessions.objects.using('mongodb').create(
#             # session_id = 'Session3',
#             session_title = 'Week 3 Python Discussion',
#             session_starttime = datetime.utcnow().__add__(timedelta(days=1,hours=5,minutes=30)),
#             session_author = 'TEST',
#             session_subject = 'subject1',
#             session_meetlink = 'https://meet.google.com/bba-rfhf-hvk',
#             session_endtime = datetime.utcnow().__add__(timedelta(days=1,hours=6,minutes=30)),
#             session_video_link = 'https://www.youtube.com/watch?v=KUECJHlV1LE&t=332s&pp=ygUnZG93bmxvYWQgaW1hZ2UgZnJvbSBkb2NrZXIgdXNpbmcgcHl0aG9u',
#             session_status = 'UPCOMING',
#             student_ids = ['25MRITCS001','student2'],
#             del_row = 'False'
#         )
#         return HttpResponse("Success")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")

# @api_view(['GET'])
# def addStudetsActivity(request,day,week):
#     try:
#         obj = students_info.objects.get( student_id = '25MRITCS001',del_row = False)
#         sub = subjects.objects.get(subject_id = 'Subject2',del_row = False)
#         topoic = topics.objects.get(topic_id = 'Topic1',del_row = False)
#         subtop = sub_topics.objects.get(sub_topic_id = 'SubTopic1',del_row = False)
#         student = student_activities.objects.create(
#             student_id = obj,
#             subject_id = sub,
#             activity_end_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#             activity_week = week,
#             activity_day = day,
#             activity_topic = topoic,
#             activity_subtopic = subtop,
#             del_row = False
#         )
#         return HttpResponse("Success")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")
# @api_view(['GET'])
# def addStudent(request):
#     try:
#         # track = tracks.objects.create(
#         #     track_id = 'Track1',
#         #     track_name =  'Engineering',
#         #     track_name_searchable = 'engineering',
#         #     track_description = 'TEST',
#         #     created_by = 'TEST',
#         #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     modified_by = 'TEST',
#         #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     action = 'TEST',
#         #     del_row = False
#         # )
#         # sub = subjects.objects.create(
#         #     subject_id = 'Subject1',
#         #     track_id = track,
#         #     subject_name =  'HTML CSS',
#         #     subject_alt_name = 'htmlcss',
#         #     subject_description = 'TEST',
#         #     created_by = 'TEST',
#         #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     modified_by = 'TEST',
#         #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     action = 'TEST',
#         #     del_row = False
#         # )
#         # sub1 = subjects.objects.create(
#         #     subject_id = 'Subject2',
#         #     track_id = track,
#         #     subject_name =  'Data Structures with C++ and Object-Oriented Programming with C++',
#         #     subject_alt_name = 'datastructureswithc++andobject-orientedprogrammingwithc++',
#         #     subject_description = 'TEST',
#         #     created_by = 'TEST',
#         #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     modified_by = 'TEST',
#         #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     action = 'TEST',
#         #     del_row = False
#         # )
#         # sub2 = subjects.objects.create(
#         #     subject_id = 'Subject3',
#         #     track_id = track,
#         #     subject_name =  'Data Structures and Algorithms',
#         #     subject_alt_name = 'datastructuresandalgorithms',
#         #     subject_description = 'TEST',
#         #     created_by = 'TEST',
#         #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     modified_by = 'TEST',
#         #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     action = 'TEST',
#         #     del_row = False
#         # )
#         # sub3 = subjects.objects.create(
#         #     subject_id = 'Subject4',
#         #     track_id = track,
#         #     subject_name =  'SQL',
#         #     subject_alt_name = 'sql',
#         #     subject_description = 'TEST',
#         #     created_by = 'TEST',
#         #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     modified_by = 'TEST',
#         #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     action = 'TEST',
#         #     del_row = False
#         # )
#         # topic = topics.objects.create(
#         #     topic_id = 'Topic1',
#         #     subject_id = sub,
#         #     topic_name =  'TEST',
#         #     topic_alt_name = 'TEST',
#         #     topic_description = 'TEST',
#         #     created_by = 'TEST',
#         #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     modified_by = 'TEST',
#         #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     action = 'TEST',
#         #     del_row = False
#         # )
#         # subtopic = sub_topics.objects.create(
#         #     sub_topic_id = 'SubTopic1',
#         #     topic_id = topic,
#         #     sub_topic_name =  'TEST',
#         #     sub_topic_description = 'TEST',
#         #     notes = 1,
#         #     videos = 1,
#         #     mcq = 1,
#         #     coding = 1,
#         #     del_row = False
#         # )
#         new = courses.objects.get(course_id = 'Course0001')
#         # create(
#         #     course_id = 'Course1',
#         #     # track_id = "None",
#         #     course_name =  'Full Stack Web Development',
#         #     course_description = 'TEST',
#         #     course_level = 'TEST',
#         #     created_by = 'TEST',
#         #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     modified_by = 'TEST',
#         #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     action = 'TEST',
#         #     del_row = False
#         # )
#         # course_subject = course_subjects.objects.create(
#         #     course_id = new,
#         #     subject_id = sub,
#         #     duration_in_days = '10',
#         #     start_date = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     end_date = datetime.utcnow().__add__(timedelta(days=10,hours=5,minutes=30)),
#         #     is_mandatory = True,
#         #     path = 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
#         #     del_row = False
#         # )
#         # course_subject1 = course_subjects.objects.create(
#         #     course_id = new,
#         #     subject_id = sub1,
#         #     duration_in_days = '10',
#         #     start_date = datetime.utcnow().__add__(timedelta(days=10,hours=5,minutes=30)),
#         #     end_date = datetime.utcnow().__add__(timedelta(days=20,hours=5,minutes=30)),
#         #     is_mandatory = True,
#         #     path = 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
#         #     del_row = False
#         # )
#         # course_subject2 = course_subjects.objects.create(
#         #     course_id = new,
#         #     subject_id = sub2,
#         #     duration_in_days = '10',
#         #     start_date = datetime.utcnow().__add__(timedelta(days=20,hours=5,minutes=30)),
#         #     end_date = datetime.utcnow().__add__(timedelta(days=30,hours=5,minutes=30)),
#         #     is_mandatory = True,
#         #     path = 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
#         #     del_row = False
#         # )
#         # course_subject3 = course_subjects.objects.create(
#         #     course_id = new,
#         #     subject_id = sub3,
#         #     duration_in_days = '10',
#         #     start_date = datetime.utcnow().__add__(timedelta(days=30,hours=5,minutes=30)),
#         #     end_date = datetime.utcnow().__add__(timedelta(days=40,hours=5,minutes=30)),
#         #     is_mandatory = True,
#         #     path = 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
#         #     del_row = False
#         # )
#         std = students_info.objects.create(
#             student_id = '25TEST00001',
#             course_id = new,
#             student_firstname = 'TEST',
#             student_lastname = ' ',
#             student_email = 'kecoview@gmail.com',
#             student_gender = 'M',
#             student_course_starttime = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#             # batch_id = 'TEST',
#             college = 'TEST',
#             branch = 'TEST',
#             address = 'TEST',    
#             phone = '132',
#             student_score = 0,
#             student_type = 'TEST',
#             linkedin = 'TEST',
#             leetcode = 'TEST',
#             hackerrank = 'TEST',
#             del_row = False
#         )
#         return HttpResponse("Added Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")

# @api_view(['GET'])
# def addstudent_app_usages(request):
#     try:
#         std = student_app_usage.objects.create(
#             student_id = '25MRITCS001',
#             # app_name = 'TEST',
#             logged_in = datetime.utcnow().__add__(timedelta(days=0,hours=5,minutes=30)),
#             logged_out = datetime.utcnow().__add__(timedelta(days=0,hours=8,minutes=30)),
#             del_row = False
#         )
#         return HttpResponse("Added Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")
# @api_view(['POST'])
# def add_course_plane_details(request):
#     try:
#         data = json.loads(request.body)

#         course = courses.objects.get(course_id = 'course3' ,del_row = False)
#         sub = subjects.objects.get(subject_id = 'Subject4' ,del_row = False)
#         print (course.id,sub.id)
#         # course_plan_detail_lastDay = course_plan_details.objects.filter(course_id = 3,del_row = False).latest('day')
#         # print('course_plan_detail_lastDay','course_plan_detail_lastDay')
#         # print(course_plan_detail_lastDay.day,data['day'])
#         # for i in range(data['day']):
#         #     week = int(i/7)+1
#         #     print(week,i+1+course_plan_detail_lastDay.day)
#         #     course_plan_detail = course_plan_details.objects.create(
#         #         course_id = course,
#         #         subject_id = sub,
#         #         day = i+1+course_plan_detail_lastDay.day,
#         #         content_type = 'study' if (i+1+course_plan_detail_lastDay.day)%7 != 0 else 'weekly test',
#         #         week = week,
#         #         day_date = datetime.utcnow().__add__(timedelta(days=i,hours=5,minutes=30)),
#         #         duration_in_hours = data['duration'],
#         #         del_row = False
#         #     )
#         plan_details = []
#         # for i in range(data['day']):
#         #     week = (i // 7) + 1
#         #     new_day = i + 1 #+ course_plan_detail_lastDay.day
#         #     plan_details.append(course_plan_details(
#         #         course_id=course,
#         #         subject_id=sub,
#         #         day=new_day,
#         #         content_type='study' if new_day % 7 != 0 else 'weekly test',
#         #         week=week,
#         #         day_date=datetime.strptime((datetime.utcnow() + timedelta(days=i+8, hours=5, minutes=30)).strftime('%Y-%m-%d'),'%Y-%m-%d'),
#         #         duration_in_hours=data['duration'],
#         #         del_row=False
#         #     ))
#         #     print(plan_details[-1].day_date)
#         week = 1
#         for i in range(data['day']):
#             # week = (i // 7) + 1

#             new_day = i + 1 #+ course_plan_detail_lastDay.day
#             plan_details.append(course_plan_details(
#                 course_id=course,
#                 subject_id=sub,
#                 day=new_day,
#                 content_type='study' if new_day % 7 != 0 else 'weekly test',
#                 week=week,
#                 day_date=datetime.strptime((datetime.utcnow() + timedelta(days=i+8, hours=5, minutes=30)).strftime('%Y-%m-%d'),'%Y-%m-%d'),
#                 duration_in_hours=data['duration'],
#                 del_row=False
#             ))
#             if plan_details[-1].day_date.weekday() == 6:
#                 week += 1
#             print(plan_details[-1].day_date,plan_details[-1].week)
#         # Bulk insert in a single query
#         # course_plan_details.objects.bulk_create(plan_details)
#         return HttpResponse("Added Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")
# @api_view(['GET'])
# def add_notification(request):
#     try:
#         std = notification.objects.using('mongodb').create(
#             notification_title = 'TEST',
#             notification_message = 'TEST',
#             notification_timestamp = datetime.utcnow().__add__(timedelta(days=0,hours=5,minutes=30)),
#             status = 'U',
#             student_id = '25MRITCS001',
#             del_row = False
#         )
#         return HttpResponse("Added Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")
# @api_view(['GET'])
# def update_student_info(request):
#     try:
#         new = courses.objects.get(course_id = 'Course1',del_row = False)
#         # create(
#         #     course_id = 'Course0001',
#         #     # track_id = "None",
#         #     course_name =  'Full Stack Web Development',
#         #     course_description = 'TEST',
#         #     course_level = 'TEST',
#         #     created_by = 'TEST',
#         #     created_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     modified_by = 'TEST',
#         #     modified_at = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#         #     action = 'TEST',
#         #     del_row = False
#         # )
#         std = students_info.objects.get(student_id = '25MRITCS001',del_row = False)
#         std.course_id = new
#         std.student_score = 50
#         std.save()
#         return HttpResponse("Updated Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")

# @api_view(['GET'])
# def add_participants(request):
#     try:
#         std = participant.objects.using('mongodb').create(
#             session_id =  36,
#             student_id = '25MRITCS001',
#             display_name = 'TEST',
#             attended_time = 4565.0,
#             del_row = 'False'
#         )
#         std1 = participant.objects.using('mongodb').create(
#             session_id =  35,
#             student_id = '25MRITCS001',
#             display_name = 'TEST',
#             attended_time = 456.0,
#             del_row = 'False'
#         )
        
#         return HttpResponse("Added Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")
# # class students_assessments(models.Model):
# #     student_id          = models.CharField(max_length=20)
# #     assessment_type = models.CharField(max_length=20)
# #     subject_id          = models.CharField(max_length=20)
# #     test_id             = models.CharField(max_length=20)
# #     course_id           = models.CharField(max_length=20)
# #     assessment_status   = models.CharField(max_length=20)
# #     assessment_score_secured = models.FloatField()
# #     assessment_max_score = models.FloatField()
# #     assessment_week_number = models.IntegerField()
# #     assessment_completion_time = models.DateTimeField()
# #     assessment_rank     = models.IntegerField()
# #     assessment_overall_rank = models.IntegerField()
# #     del_row = models.CharField(default='False',max_length=5)
# @api_view(['GET'])
# def add_std_testDetails(request):
#     try:
#         std = students_assessments.objects.using('mongodb').create(
#             student_id = '25MRITCS001',
#             assessment_type = 'Weekly Test',
#             subject_id = 'Subject4',
#             test_id = 'Test1',
#             course_id = 'Course0001',
#             assessment_status = 'Ongoing',
#             assessment_score_secured = 0,
#             assessment_max_score = 0,
#             assessment_week_number = 1,
#             assessment_completion_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#             assessment_rank = 0,
#             assessment_overall_rank = 0,
#             del_row = 'False'
#         ) 
#         std2 = students_assessments.objects.using('mongodb').create(
#             student_id = '25MRITCS001',
#             assessment_type = 'Weekly Test',
#             subject_id = 'Subject4',
#             test_id = 'Test2',
#             course_id = 'Course0001',
#             assessment_status = 'Upcoming',
#             assessment_score_secured = 0,
#             assessment_max_score = 0,
#             assessment_week_number = 1,
#             assessment_completion_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#             assessment_rank = 0,
#             assessment_overall_rank = 0,
#             del_row = 'False'
#         )
#         std3 = students_assessments.objects.using('mongodb').create(
#             student_id = '25MRITCS001',
#             assessment_type = 'Weekly Test',
#             subject_id = 'Subject4',
#             test_id = 'Test3',
#             course_id = 'Course0001',
#             assessment_status = 'Completed',
#             assessment_score_secured = 10.0,
#             assessment_max_score = 10.0,
#             assessment_week_number = 1,
#             assessment_completion_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#             assessment_rank = 0,
#             assessment_overall_rank = 0,
#             del_row = 'False'
#         )
#         return HttpResponse("Added Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")
# @api_view(['GET'])
# def add_testDetails(request):
#     try:
#         course = courses.objects.get(course_id = 'Course0001' ,del_row = False)
#         sub = subjects.objects.get(subject_id = 'Subject4' ,del_row = False)
#         track = tracks.objects.get(track_id = 'Track1' ,del_row = False)
#         test = test_details.objects.create(
#             test_id = 'Test1',
#             test_name = 'week 1 test',
#             test_duration = '10',
#             test_marks = 10,
#             test_type = 'Weekly Test',
#             test_description = 'weekly test',
#             test_created_by = 'rahul',
#             track_id = track,
#             course_id = course,
#             subject_id = sub,
#             level = 'Beginner',
#             tags = 'test',
#             test_date_and_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#             del_row = 'False'
#         )
#         test1 = test_details.objects.create(
#             test_id = 'Test2',
#             test_name = 'week 2 test',
#             test_duration = '50',
#             test_marks = 50,
#             test_type = 'Weekly Test',
#             test_description = 'weekly test',
#             test_created_by = 'rahul',
#             track_id = track,
#             course_id = course,
#             subject_id = sub,
#             level = 'Beginner',
#             tags = 'test',
#             test_date_and_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#             del_row = 'False'
#         )
#         test2 = test_details.objects.create(
#             test_id = 'Test3',
#             test_name = 'week 3 test',
#             test_duration = '100',
#             test_marks = 100,
#             test_type = 'Weekly Test',
#             test_description = 'weekly test',
#             test_created_by = 'rahul',
#             track_id = track,
#             course_id = course,
#             subject_id = sub,
#             level = 'Beginner',
#             tags = 'test',
#             test_date_and_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#             del_row = 'False'
#         )
#         return HttpResponse("Added Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")
    
# @api_view(['GET'])
# def add_test_sction(request):
#     try:
#         tests = test_details.objects.filter(test_id__in = ['Test1','Test2','Test3'] ,del_row = False)
#         topic_s = topics.objects.get(topic_id = 'Topic1' ,del_row = False)
#         sub_topic_s = sub_topics.objects.get(sub_topic_id = 'SubTopic1' ,del_row = False)
#         j =1
#         for i in tests:
#             test_section = test_sections.objects.create(
#                 test_id = i,
#                 section_name = 'Section1',
#                 topic_id = topic_s,
#                 sub_topic_id = sub_topic_s,
#                 question_id = questions.objects.create(
#                     question_id = 'Question'+str(j),
#                     question_type = 'MCQ',
#                     level = 'Beginner',
#                     created_by = 'Rahul',
#                     creation_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#                     last_updated_time = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
#                     last_updated_by = 'Rahul',
#                     reviewed_by = 'Rahul',
#                     tags = 'test',
#                     sub_topic_id = sub_topic_s,
#                     del_row = 'False'
#                 ),
#                 del_row = 'False'
#             )
#             j+=1
#         return HttpResponse("Added Successfully")
#     except Exception as e:
#         print(e)
#         return HttpResponse("Failed")
            