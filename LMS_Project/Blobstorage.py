import json
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
    return cache.get(blob_name)

# def get_blob_list(blob_name):
#     blob_client = get_blob_container_client().get_blob_client(blob_name)