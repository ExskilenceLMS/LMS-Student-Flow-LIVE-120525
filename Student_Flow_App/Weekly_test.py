
from LMS_Project.Blobstorage import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from LMS_MSSQLdb_App.models import *
from LMS_Mongodb_App.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Max, F ,Sum,Min,Count
# from django.contrib.postgres.aggregates import ArrayAgg
import json
from django.db.models.functions import TruncDate    

rule_for_weekly_test = {
    'MCQ':10,'Coding':3
}

@api_view(['GET'])
def Automated_weekly_test(request,student_id,week_number,subject_id): 
    try:
        student_detaile = students_details.objects.using('mongodb').get(student_id = student_id,del_row = False)
        week_status = []
        all_sub_topics =[]
        all_practice_Questions = []
        for day in student_detaile.student_question_details.get(subject_id).get('week_'+str(week_number)):
            day = student_detaile.student_question_details.get(subject_id).get('week_'+str(week_number)).get(day)
            [ week_status.append(day.get('sub_topic_status').get(sub,0)==2) for sub in day.get('sub_topic_status')]
            all_practice_Questions.extend(day.get('mcq_questions'))
            all_practice_Questions.extend(day.get('coding_questions'))
            all_sub_topics.extend([sub for sub in day.get('sub_topic_status')])
        if week_status.count(True) == len(week_status):
            sub_topic_wise_mcq_qns = {}
            sub_topic_wise_coding_qns = {}
            sub_topic_wise_mcq_qns.update({sub :[] for sub in all_sub_topics})
            sub_topic_wise_coding_qns.update({sub :[] for sub in all_sub_topics})
            print('completed',all_sub_topics)
            Qns_list_obj = questions.objects.filter(sub_topic_id__sub_topic_id__in=all_sub_topics,del_row=False) 
            [sub_topic_wise_mcq_qns.get(qn.sub_topic_id.sub_topic_id).append(qn.question_id) for qn in Qns_list_obj if qn.question_id not in all_practice_Questions and str(qn.question_id)[-5].lower()=='m']
            [sub_topic_wise_coding_qns.get(qn.sub_topic_id.sub_topic_id).append(qn.question_id) for qn in Qns_list_obj if qn.question_id not in all_practice_Questions and str(qn.question_id)[-5].lower()=='c']
            all_mcq_qns = []
            all_coding = []
            while len(all_mcq_qns)< rule_for_weekly_test.get('MCQ') or len(all_coding)< rule_for_weekly_test.get('Coding') :
                if  len(sub_topic_wise_mcq_qns.get(sub_qn))==0 and  len(sub_topic_wise_coding_qns.get(sub_qn))==0:
                    break
                for sub_qn in sub_topic_wise_mcq_qns:
                    if len(sub_topic_wise_mcq_qns.get(sub_qn)) >0 :
                        mcq_qns = random.sample(sub_topic_wise_mcq_qns.get(sub_qn),len(sub_topic_wise_mcq_qns.get(sub_qn)))
                        if len(all_mcq_qns)< rule_for_weekly_test.get('MCQ'):
                            qn = mcq_qns[0]
                            all_mcq_qns.append(qn)
                        sub_topic_wise_mcq_qns.get(sub_qn).pop(qn)
                    if  len(sub_topic_wise_coding_qns.get(sub_qn))>0:
                        codin_qns = random.sample(sub_topic_wise_coding_qns.get(sub_qn),len(sub_topic_wise_coding_qns.get(sub_qn)))
                        if len(all_coding)< rule_for_weekly_test.get('Coding'):
                            qn = codin_qns[0]
                            all_coding.append(qn)
                            sub_topic_wise_coding_qns.get(sub_qn).pop(qn)
                    
                    print(sub_qn)
                    print()
            # container_client =  get_blob_container_client()
            # for subtop in all_sub_topics:
            #     cacheed_lists = cache.get(f'subjects/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type.lower()}/')
            #     if cacheed_lists:
            #         cache.set(f'subjects/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type.lower()}/',cacheed_lists)
            #         all_qns_list = cacheed_lists
            #     else:
            #         all_qns_list =container_client.list_blobs(
            #                         name_starts_with =f'subjects/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type.lower()}/')
            #         cache.set(f'subjects/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type.lower()}/',all_qns_list)
            #     all_qns = [blob.name.split('/')[-1].split('.')[0] for blob in all_qns_list]
            return JsonResponse(all_practice_Questions,safe=False,status=200)
        else:
            return JsonResponse({"message": "Not Unlocked yet"},safe=False,status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)