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

# FETCH STUDENT LEARNING MODULEs

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
    
# ADD DAILY QUESTIONS 

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
        else:
            sub_topics  = [ i[1:-5]  for i in student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))).get('mcq_questions_status')]
            response.update({'message':'not updated',
                             'sub_topics':sub_topics,
                             'data':student.student_question_details.get(data.get('subject')).get('week_'+str(data.get('week_number'))).get('day_'+str(data.get('day_number'))).get('mcq_questions_status')})
        
        return JsonResponse(response,safe=False,status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Failed","error":str(e)},safe=False,status=400)
    
# FETCH OVERVIEW

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
    
# FETCH QUESTIONS

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

# SUBMIT MCQ QUESTION  

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
        de_buging = de_buging + '0.3 '
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
    
# SUBMIT CODING QUESTION

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