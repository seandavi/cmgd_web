import uuid
import base64
import json
import structlog

import sqlalchemy as sa

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

import datetime
from _datetime import timezone

from ..models.files import StorageEvent
from ..models import db

logger = structlog.getLogger()

router = APIRouter()

class StorageEventModel(BaseModel):
    kind: str
    id: str
    self_link: str = Field(alias="selfLink")
    name: str
    bucket: str
    generation: int
    metageneration: int
    content_type: str = Field(alias="contentType",
                              description = "The MIME type of the object")
    created: datetime.datetime = Field(alias="timeCreated")
    updated: datetime.datetime
    size: int
    md5_hash: str = Field(alias="md5Hash")
    media_link: str = Field(alias="mediaLink")
    content_language: str = Field(alias = "contentLanguage", default=None)
    crc32c: str
    etag: str
    event_type: str = Field(alias = "eventType")
    event_time: datetime.datetime = Field(alias="eventTime")

    class Config:
        # see https://medium.com/analytics-vidhya/camel-case-models-with-fast-api-and-pydantic-5a8acb6c0eee
        allow_population_by_field_name = True


class StorageEventReturn(StorageEventModel):
    event_id: uuid.UUID
    download_url: str


class StorageEventCollection(BaseModel):
    hits: List[StorageEventReturn]


def init_app(app):
    app.include_router(router, prefix='/files')

@router.post('/changes')
async def files_change(event: dict):
    """Track all changes in cloud storage"""
    message = event['message']
    payload = base64.b64decode(message['data']).decode('UTF-8')
    del(message['data'])
    payload2 = json.loads(payload)
    payload2.update(message['attributes'])
    event = StorageEventModel(**payload2)
    t = StorageEvent.__table__

    query = t.insert().values(**event.dict())
    logger.msg("INFO",message=event.dict())
    db_event = await db.execute(query)

    return db_event

@router.get("/changes", response_model=StorageEventCollection)
async def list_file_events(
        limit: int=100,
        offset: int=0,
        start_date: datetime.date=None,
        end_date: datetime.date=None,
        filename_regex: str=None
) -> StorageEventCollection:
    t = StorageEvent.__table__
    query = t.select()
    if(start_date):
        query = query.where(StorageEvent.updated>start_date)
    if(end_date):
        query = query.where(StorageEvent.updated<end_date)
    if(filename_regex):
        query = query.where(sa.text('name ~ :reg')).params(reg=filename_regex)
    events_query = query.limit(limit).offset(offset)
    events = await db.fetch_all(events_query)
    def get_full_event_entry(event):
        event = dict(event.items())
        event['download_url']=generate_download_signed_url_v4(event['name'])

        return event

    return {"hits": list([get_full_event_entry(event) for event in events])}


from google.cloud import storage

@router.get('/signed')
def generate_download_signed_url_v4(name: str):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    bucket_name = 'data-curatedmetagenomics'
    #name = 'your-object-name'

    from google.oauth2 import service_account
    import os

    KEYFILE = 'curatedmetagenomicdata-60b3f98b417c.json'
    PROJECT = 'curatedmetagenomicdata'

    credentials = service_account.Credentials.from_service_account_file(KEYFILE)

    storage_client = storage.Client(project=PROJECT, credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(name)
    filename = blob.name.split('/')[blob.name.count('/')]

    url = blob.generate_signed_url(
        version="v4",
        response_disposition=f'attachment; filename={filename}',
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=30),
        # Allow GET requests using this URL.
        method="GET",
    )
    return url






def BAD_generate_download_signed_url_v4(name: str):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'
    import os

    KEYFILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    PROJECT = 'curatedmetagenomics'
    print(KEYFILE)

    import google.auth
    from google.oauth2 import service_account
    from google.auth.transport import requests
    from google.auth import compute_engine

    credentials, project = google.auth.default()

    bucket_name='data-curatedmetagenomics'
    storage_client = storage.Client(project, credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(name)

    auth_request = requests.Request()

    signing_credentials = compute_engine.IDTokenCredentials(
        auth_request, "",
        service_account_email=credentials.service_account_email)

    url = blob.generate_signed_url(
        credentials = signing_credentials,
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )

    print("Generated GET signed URL:")
    print(url)
    print("You can use this URL with any user agent, for example:")
    print("curl '{}'".format(url))
    return url
