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
from .AppUsage import update_app_usage, create_app_usage
from django.core.cache import cache
ONTIME = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
CONTAINER ="internship"
@api_view(['GET'])   
def home(request):
    return JsonResponse({"message": "Successfully Deployed LMS on Azure at "+ str(ONTIME)},safe=False,status=200)

@api_view(['GET'])
def  LogIn (request,email):
    try:
        user = students_info.objects.get(student_email = email,
                                         del_row = False)
        create_app_usage( user.student_id)
        return JsonResponse({"message": "Successfully Logged In",
                             "student_id":user.student_id,
                             'course_id':user.course_id.course_id},safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
@api_view(['GET'])
def LogOut (request, student_id):
    try:
        update_app_usage(student_id)
        return JsonResponse({"message": "Successfully Logged Out"},safe=False,status=200)
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
# from django.db.models import Q 
# @api_view(['GET'])
# def get_all_tracks(request):
#     if request.method == "GET":
#         try:
#             tracks_data = tracks.objects.filter(del_row=False)
#             tracks_names = [track.track_name for track in tracks_data]
#             query = Q()
#             for track_name in tracks_names:
#                 query |= Q(tracks__icontains=track_name)
#             Courses = courses.objects.filter(query, del_row=False)
#             data=[]
#             track_data ={}
#             for track in tracks_data:
#                 d={
#                     "track_id":track.track_id,
#                     "track_name": track.track_name,
#                     "track_name_searchable": track.track_name_searchable,
#                     "track_description": track.track_description,
#                 }
#                 track_data.update({track.track_name:d})
#             for course in Courses:
#                 for i in course.tracks.split(","):
#                     d={
#                         "course_id":course.course_id,
#                         "course_name": course.course_name,
#                     }
#                     d.update(track_data.get(str(i)))
#                     # data.append(d)
                    
#             return JsonResponse({'tracks': data})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
