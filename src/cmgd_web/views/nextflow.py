#!/usr/bin/env python3
import uuid
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

from ..models.nextflow import NextflowEvent
import datetime
from _datetime import timezone

router = APIRouter()


def init_app(app):
    app.include_router(router, prefix='/nextflow')


class NextflowEventModel(BaseModel):
    run_name: str = Field(alias="runName")
    run_id: uuid.UUID = Field(alias="runId")
    event: str
    utc_time: datetime.datetime = Field(
        alias="utcTime")
    trace: dict=None
    metadata: dict=None
   

class NextflowEventReturn(NextflowEventModel):
    """Represents a nextflow event
    """
    event_id: int


class NextflowEventCollection(BaseModel):
    """Represents a nextflow event
    """
    hits: List[NextflowEventReturn]


@router.get('/events')
async def list_nextflow_events() -> NextflowEventCollection:
    events = await NextflowEvent.query.gino.all()
    return {"hits": list([event.to_dict() for event in events])}


@router.post('/events')
async def add_nextflow_event(event: NextflowEventModel):
    db_event = await NextflowEvent(**event.dict()).create()
    return db_event

@router.get("/events/{id}")
async def get_nextflow_event(id: uuid.UUID):
    event = await NextflowEvent.get_or_404(id)
    return event.to_dict()
