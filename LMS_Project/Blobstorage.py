import json
import random
from azure.storage.blob import BlobServiceClient
from .settings import *
from django.core.cache import cache

def get_blob_service_client():
    account_name = AZURE_ACCOUNT_NAME
    account_key = AZURE_ACCOUNT_KEY
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    return BlobServiceClient.from_connection_string(connection_string)
def get_blob_container_client():
    account_name = AZURE_ACCOUNT_NAME
    account_key = AZURE_ACCOUNT_KEY
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    return BlobServiceClient.from_connection_string(connection_string).get_container_client(AZURE_CONTAINER)

def get_blob(blob_name):
    cacheresponse = cache.get(blob_name)
    if cacheresponse:
        print('cache hit')
        cache.set(blob_name,cacheresponse)
        return cacheresponse
    blob_client = get_blob_container_client().get_blob_client(blob_name)
    cache.set(blob_name,blob_client.download_blob().readall())
    # return blob_client.download_blob().readall()
    blob_client.close()
    return cache.get(blob_name)

def get_list_blob(blob_path,list_of_qns,type):
    container_client =  get_blob_container_client()
    files = []
    for Qn in list_of_qns:
        path = f'{blob_path}{Qn[1:3]}/{Qn[1:-7]}/{Qn[1:-5]}/{type}/{Qn}.json'
        blob_client = container_client.get_blob_client(path)
        blob_data = json.loads(blob_client.download_blob().readall())
        blob_data.update({ "Qn_name": Qn})
        files.append(blob_data)
    container_client.close()
    return files
def get_random_questions(types,subtops,levels):
    container_client =  get_blob_container_client()
    files = {}
    blob_client = container_client.get_blob_client('LMS_Rules/Rules.json')
    Rules = json.loads(blob_client.download_blob().readall())
    for type in types:
        for subtop in subtops:
            all_qns =[blob.name.split('/')[-1].split('.')[0] for blob in container_client.list_blobs(
                name_starts_with=f'LMSData/{subtop[0:2]}/{subtop[0:-2]}/{subtop}/{type}/')]
            Qns  = random.sample([qn for qn in all_qns if qn[-4]=='e'], levels.get(type,{}).get(subtop,{}).get('level1',0))
            Qns.extend(random.sample([qn for qn in all_qns if qn[-4]=='m'], levels.get(type,{}).get(subtop,{}).get('level2',0)))
            Qns.extend(random.sample([qn for qn in all_qns if qn[-4]=='h'], levels.get(type,{}).get(subtop,{}).get('level3',0)))
            score = 0
            for level in Rules.get(type.lower(),[]):
                level_score = int(levels.get(type,{}).get(subtop,{}).get(level.get('level').lower(),0))*int(level.get('score'))
                score = score +level_score
            files.update({type:Qns,
                          type+'_score':score})
    container_client.close()
    return files
# def get_blob_list(blob_name):
#     container_client = get_blob_container_client()

#     blob_list = container_client.list_blobs(name_starts_with=blob_name)
    
#     for blob in blob_list:
#         blob_client = container_client.get_blob_client(blob['name'])
#         blob_properties = blob_client.get_blob_properties()

#         print(f"Blob Name: {blob['name']}")
#         print(f"Last Modified: {blob_properties['last_modified']}")
#         print(f"Blob Size: {blob_properties['size']} bytes")
#         print(f"Blob Content Type: {blob_properties['content_settings'].content_type}")

#     return blob_list