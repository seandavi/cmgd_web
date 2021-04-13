#!/usr/bin/env python3
import uuid
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

from ..models.nextflow import nextflow_event
from ..models import db
import datetime
from _datetime import timezone

router = APIRouter()


def init_app(app):
    app.include_router(router, prefix='/nextflow')


class NFModel(BaseModel):
    run_name: str = Field()
    run_id: uuid.UUID = Field()
    event: str
    utc_time: datetime.datetime = Field()
    trace: dict = None
    metadata: dict = None
   

class NFReturn(NFModel):
    """Represents a nextflow event
    """
    event_id: int


class NFCollection(BaseModel):
    """Represents a nextflow event
    """
    hits: List[NFReturn]


@router.get('/events', response_model = NFCollection)
async def list_nextflow_events(limit: int=100, offset: int=0) -> NFCollection:
    query = nextflow_event.select().limit(limit).offset(offset)
    events = await db.fetch_all(query)
    return NFCollection(hits = list([event.items() for event in events]))


@router.post('/events')
async def add_nextflow_event(event: NFModel):
    """Events from running Nextflow pipelines when using -with-weblog.

    See [the Nextflow documentation](https://www.nextflow.io/docs/latest/tracing.html#weblog-via-http).
    """
    t = nextflow_event
    query = t.insert().values(**event.dict())
    db_event = await db.execute(query)
    return db_event

@router.get("/events/{id}")
async def get_nextflow_event(id: uuid.UUID):
    event = await NF.get_or_404(id)
    return event.to_dict()

