import uuid
import base64
import json

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

import datetime
from _datetime import timezone

from ..models.files import StorageEvent

router = APIRouter()

class StorageEventModel(BaseModel):
    kind: str
    id: str
    self_link: str = Field(alias="selfLink")
    name: str
    bucket: str
    generation: int
    metageneration: int
    content_type: str = Field(alias="contentType")
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


class StorageEventReturn(StorageEventModel):
    event_id: uuid.UUID


class StorageEventCollection(BaseModel):
    hits: List[StorageEventReturn]


def init_app(app):
    app.include_router(router, prefix='/files')

@router.post('/changes')
async def files_change(event: dict):
    message = event['message']
    payload = base64.b64decode(message['data']).decode('UTF-8')
    del(message['data'])
    payload2 = json.loads(payload)
    payload2.update(message['attributes'])
    print(payload2)
    event = StorageEventModel(**payload2)
    db_event = await StorageEvent(**event.dict()).create()
    return db_event

@router.get("/changes")
async def list_file_events(limit: int=100, offset: int=0) -> StorageEventCollection:
    events = await StorageEvent.query.limit(limit).offset(offset).gino.all()
    return {"hits": list([event.to_dict() for event in events])}
