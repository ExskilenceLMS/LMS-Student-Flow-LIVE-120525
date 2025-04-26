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
# from LMS_Project.Blobstorage import *
from .AppUsage import update_app_usage
from django.core.cache import cache



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
            update_app_usage(student_id)
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
        update_app_usage(student_id)
        return JsonResponse({'test_details':response},safe=False,status=200)
    except Exception as e:
        print(e)
        update_app_usage(student_id)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
