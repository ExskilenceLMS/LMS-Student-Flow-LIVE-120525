
from LMS_Project.Blobstorage import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from LMS_MSSQLdb_App.models import *
from LMS_Mongodb_App.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Max, F ,Sum,Min,Count
from django.db.models.functions import Substr, Cast
from django.db.models import IntegerField
# from django.contrib.postgres.aggregates import ArrayAgg
import json
from django.db.models.functions import TruncDate    

rule_for_weekly_test = {
    'MCQ':10,'Coding':3
    # 'MCQ':7,'Coding':3
}

# @api_view(['GET'])
# def Automated_weekly_test(request,student_id,week_number,subject_id): 
#     try:
#         student_detaile = students_details.objects.using('mongodb').get(student_id = student_id,del_row = False)
#         week_status = []
#         all_sub_topics =[]
#         all_practice_Questions = []
#         for day in student_detaile.student_question_details.get(subject_id).get('week_'+str(week_number)):
#             day = student_detaile.student_question_details.get(subject_id).get('week_'+str(week_number)).get(day)
#             [ week_status.append(day.get('sub_topic_status',{}).get(sub,0)==2) for sub in day.get('sub_topic_status',{})]
#             all_practice_Questions.extend(day.get('mcq_questions',[]))
#             all_practice_Questions.extend(day.get('coding_questions',[]))
#             all_sub_topics.extend([sub for sub in day.get('sub_topic_status',{})])
#         if week_status.count(True) == len(week_status):
#             sub_topic_wise_mcq_qns = {}
#             sub_topic_wise_coding_qns = {}
#             sub_topic_wise_mcq_qns.update({sub :[] for sub in all_sub_topics})
#             sub_topic_wise_coding_qns.update({sub :[] for sub in all_sub_topics})
#             print('completed',all_sub_topics)
#             Qns_list_obj = questions.objects.filter(sub_topic_id__sub_topic_id__in=all_sub_topics,del_row=False) 
#             [sub_topic_wise_mcq_qns.get(qn.sub_topic_id.sub_topic_id).append(qn.question_id) for qn in Qns_list_obj if qn.question_id not in all_practice_Questions and str(qn.question_id)[-5].lower()=='m']
#             [sub_topic_wise_coding_qns.get(qn.sub_topic_id.sub_topic_id).append(qn.question_id) for qn in Qns_list_obj if qn.question_id not in all_practice_Questions and str(qn.question_id)[-5].lower()=='c']
#             all_mcq_qns = []
#             all_coding = []
#             print(len(all_mcq_qns)< rule_for_weekly_test.get('MCQ'),len(all_coding)< rule_for_weekly_test.get('Coding'))
#             while len(all_mcq_qns)< rule_for_weekly_test.get('MCQ') or len(all_coding)< rule_for_weekly_test.get('Coding') :
#                 # if  len(sub_topic_wise_mcq_qns.get(sub_qn))==0 and  len(sub_topic_wise_coding_qns.get(sub_qn))==0:
#                 #     break
#                 for sub_qn in all_sub_topics:
#                     print('1',sub_topic_wise_mcq_qns.get(sub_qn))
#                     if len(sub_topic_wise_mcq_qns.get(sub_qn)) >0 :
#                         # print('1.1')
#                         mcq_qns = random.sample(sub_topic_wise_mcq_qns.get(sub_qn),len(sub_topic_wise_mcq_qns.get(sub_qn)))
#                         # print('1.2')
#                         qn = mcq_qns[0]
#                         if len(all_mcq_qns)< rule_for_weekly_test.get('MCQ'):
#                             all_mcq_qns.append(qn)
#                             print('1.3',qn)
#                         sub_topic_wise_mcq_qns.get(sub_qn).remove(qn)
                    
#                     if  len(sub_topic_wise_coding_qns.get(sub_qn))>0:
#                         print('2',sub_topic_wise_coding_qns.get(sub_qn))
#                         codin_qns = random.sample(sub_topic_wise_coding_qns.get(sub_qn),len(sub_topic_wise_coding_qns.get(sub_qn)))
#                         # print('3')
#                         cqn = codin_qns[0]
#                         if len(all_coding)< rule_for_weekly_test.get('Coding'):
#                             # print('4',cqn)
#                             all_coding.append(cqn)
#                         print('4',cqn)
#                         sub_topic_wise_coding_qns.get(sub_qn).remove(cqn)
#                         print('4',sub_topic_wise_coding_qns.get(sub_qn))
#                         # print('5')
                    
#                     print(all_mcq_qns ,all_coding)
#                     print()
#             # container_client =  get_blob_container_client()
#             # for subtop in all_sub_topics:
#             #     cacheed_lists = cache.get(f'subjects/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type.lower()}/')
#             #     if cacheed_lists:
#             #         cache.set(f'subjects/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type.lower()}/',cacheed_lists)
#             #         all_qns_list = cacheed_lists
#             #     else:
#             #         all_qns_list =container_client.list_blobs(
#             #                         name_starts_with =f'subjects/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type.lower()}/')
#             #         cache.set(f'subjects/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type.lower()}/',all_qns_list)
#             #     all_qns = [blob.name.split('/')[-1].split('.')[0] for blob in all_qns_list]
#             return JsonResponse(all_practice_Questions,safe=False,status=200)
#         else:
#             return JsonResponse({"message": "Not Unlocked yet"},safe=False,status=400)
#     except Exception as e:
#         print(e)
#         return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)


@api_view(['GET'])
def Automated_weekly_test(request,student_id,week_number,subject_id): 
    try:
        student_detaile = students_details.objects.using('mongodb').get(student_id = student_id,del_row = False)
        week_status = []
        all_sub_topics =[]
        sections = {}
        all_practiced_Questions = []
        for day in student_detaile.student_question_details.get(subject_id).get('week_'+str(week_number)):
            day = student_detaile.student_question_details.get(subject_id).get('week_'+str(week_number)).get(day)
            [ week_status.append(day.get('sub_topic_status',{}).get(sub,0)==2) for sub in day.get('sub_topic_status',{})]
            all_practiced_Questions.extend(day.get('mcq_questions',[]))
            all_practiced_Questions.extend(day.get('coding_questions',[]))
            all_sub_topics.extend([sub for sub in day.get('sub_topic_status',{})])
        if week_status.count(True) == len(week_status):
            sub_topic_wise_mcq_qns = {}
            sub_topic_wise_coding_qns = {}
            sub_topic_wise_mcq_qns.update({sub :[] for sub in all_sub_topics})
            sub_topic_wise_coding_qns.update({sub :[] for sub in all_sub_topics})
            Qns_list_obj = questions.objects.filter(sub_topic_id__sub_topic_id__in=all_sub_topics,\
                                                    sub_topic_id__topic_id__subject_id__subject_id = subject_id,\
                                                    del_row=False) 
            all_Qns =[]
            all_mcq_qns = []
            all_coding = []
            mcqsection =[]
            codingsections=[]
            for qn in Qns_list_obj:
                if  str(qn.question_id)[-5].lower()=='m':
                    sub_topic_wise_mcq_qns.get(qn.sub_topic_id.sub_topic_id).append(qn.question_id)
                    all_mcq_qns.append(qn.question_id)
                if  str(qn.question_id)[-5].lower()=='c':
                    sub_topic_wise_coding_qns.get(qn.sub_topic_id.sub_topic_id).append(qn.question_id)
                    all_coding.append(qn.question_id)
                all_Qns.append(qn.question_id)
            maxMCQ = rule_for_weekly_test.get('MCQ')
            maxCoding = rule_for_weekly_test.get('Coding')

            if len(all_mcq_qns) < maxMCQ:
                if len(all_coding) >= (maxCoding + round((maxMCQ-len(all_mcq_qns))/2)):
                    maxCoding+=round((maxMCQ-len(all_mcq_qns))/2)
                   
                else :
                    maxCoding =(maxCoding + round((maxMCQ-len(all_mcq_qns))/2) )
                maxMCQ=maxMCQ-(maxMCQ-len(all_mcq_qns))
            if len(all_coding) < maxCoding:
                if len(all_mcq_qns) >= (maxMCQ + round((maxCoding-len(all_coding))*2)):
                    maxMCQ+=round((maxCoding-len(all_coding))*2)
                    # maxCoding=maxCoding-(maxCoding-len(all_coding))
                else:
                    maxMCQ =(maxMCQ + round((maxCoding-len(all_coding))*2))
                maxCoding =maxCoding-(maxCoding-len(all_coding))
            while True:
                if all_Qns ==[]  :
                    print('break by allQNS')
                    break
                if all_mcq_qns ==[]  :
                    print('break by all_mcq_qns')
                    break
                if all_coding ==[]  :
                    print('break by all_coding')
                    break
                for sub_qn in all_sub_topics:
                    if len(sub_topic_wise_mcq_qns.get(sub_qn)) >0 :
                        mcq_qns = random.sample(sub_topic_wise_mcq_qns.get(sub_qn),len(sub_topic_wise_mcq_qns.get(sub_qn)))
                        qn = mcq_qns[0]
                        if len(mcqsection)< maxMCQ:
                            mcqsection.append(qn)
                        sub_topic_wise_mcq_qns.get(sub_qn).remove(qn) 
                        all_Qns.remove(qn)
                        all_mcq_qns.remove(qn)             
                    if  len(sub_topic_wise_coding_qns.get(sub_qn))>0:
                        codin_qns = random.sample(sub_topic_wise_coding_qns.get(sub_qn),len(sub_topic_wise_coding_qns.get(sub_qn)))
                        cqn = codin_qns[0]
                        if len(codingsections)< maxCoding:
                            codingsections.append(cqn)
                        sub_topic_wise_coding_qns.get(sub_qn).remove(cqn)
                        all_Qns.remove(cqn)
                        all_coding.remove(cqn)
                    

            sections.update({'all_Qns':all_Qns,'mcq':sub_topic_wise_mcq_qns,
                             'ciding':sub_topic_wise_coding_qns,
                             'sections':{
                                 'mcq':mcqsection,'coding':codingsections
                             }})
           
            return JsonResponse(sections,safe=False,status=200)
        else:
            return JsonResponse({"message": "Not Unlocked yet"},safe=False,status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
    
def create_weekly_test():
    try:
        test_count = test_details.objects.annotate(
         test_number=Cast(Substr('test_id', 5), IntegerField())  # 'Test' is 4 characters
                ).order_by('-test_number').first()
        # data = json.loads(request.body)
        test = test_details.objects.create(
            test_id = 'Test'+str( test_count.test_number+1 if test_count !=None else 0+1) ,#auto generated like test1, test2
            test_name = 'Week '+str()+' Test',
            test_description = 'Weekly test for Week '-str(), 
            test_duration = '60',
            test_marks = 10,
            test_type = 'Weekly Test',
            track_id = '',                
            course_id     = '',          
            subject_id         = '',     
            topic_id= '',
            test_created_by = "Auto generated",
            test_created_date_time = timezone.now().__add__(timedelta(hours=5,minutes=30)),
        )

        return JsonResponse({"status": "success",
                             'test_id': test.test_id})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "error","message":str(e)})