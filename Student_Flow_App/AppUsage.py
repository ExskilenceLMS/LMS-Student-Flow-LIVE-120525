
from LMS_MSSQLdb_App.models import *
from LMS_Mongodb_App.models import *
from django.db.models import Max, F ,Sum
from django.http import JsonResponse
from datetime import datetime, timedelta

def update_app_usage(student_id):
    try:
        student_app_usages = student_app_usage.objects.filter(
            student_id = student_id,del_row = False).order_by('-logged_out').first()

        if student_app_usages:
            student_app_usages.logged_out = datetime.utcnow().__add__(timedelta(hours=5,minutes=30))
            student_app_usages.save()

        return 
    except Exception as e:
        print(e)
        return 
def create_app_usage(student_id):
    try:
        student_app_usages = student_app_usage.objects.create(
            student_id = student_id,
            # app_name = 'TEST',
            logged_in = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            logged_out = datetime.utcnow().__add__(timedelta(hours=5,minutes=30)),
            del_row = False
        )
        return  
    except Exception as e:
        print(e)
        return