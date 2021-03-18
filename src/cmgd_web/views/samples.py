from uuid import UUID
import base64
import json

import sqlalchemy as sa
from ..models import db
from ..utils.uuid_gen import uuid_from_string

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

import datetime
from _datetime import timezone

from ..models.samples import (studies, samples, variables, samples_to_studies)


router = APIRouter()

def init_app(app):
    app.include_router(router, prefix='/metadata')


class Study(BaseModel):
    name: str
    pubmed: int = Field(description="A single pubmed id")

class StudyReturn(Study):
    uuid: UUID

class Sample(BaseModel):
    name: str
    hash: str=None

class SampleReturn(Sample):
    uuid: UUID

@router.get('/uuid')
def get_uuid_from_string(string: str):
    return str(uuid_from_string(string))


@router.post('/studies')
async def create_study(study: Study) -> StudyReturn:
    print(study.dict())
    query = studies.insert().values(**study.dict())
    ret_uuid = await db.execute(query)
    return StudyReturn(uuid=ret_uuid, **study.dict())

@router.get('/studies')
async def get_studies() -> List[StudyReturn]:
    query = studies.select()
    ret = await db.fetch_all(query)
    return [StudyReturn(**r) for r in ret]

@router.get('/studies/{uuid}/samples')
async def samples_for_study(uuid: UUID) -> List[SampleReturn]:
    query = (sa.select([samples,samples_to_studies.c.study_uuid])
             .select_from(
                 samples.join(samples_to_studies))
             .where(samples_to_studies.c.study_uuid==uuid))
    ret = await db.fetch_all(query)
    return [SampleReturn(**r) for r in ret]

@router.delete('/studies/{uuid}')
async def delete_study(uuid: UUID):
    query = studies.delete().where(studies.c.uuid==uuid)
    res = await db.execute(query)
    return res

@router.get('/samplesjson')
async def samples_json():
    query = sa.text("""select samples.*,jsonb_agg(s.j) from samples join (select sample_uuid,row_to_json(studies) j from
    samples_to_studies join studies ON studies.uuid = samples_to_studies.study_uuid) s on s.sample_uuid=samples.uuid group by samples.uuid;""")
    ret = await db.fetch_all(query)
    return ret

@router.post('/samples')
async def create_sample(sample: Sample) -> SampleReturn:
    async with db.transaction():
        params = {'name': sample.name}
        if(sample.hash is not None):
            params['hash']=hash
        query = samples.insert().values(**params)
        ret_uuid = await db.execute(query)
        query = samples_to_studies.insert().values(
            sample_uuid=ret_uuid, study_uuid=sample.study_uuid)
        await db.execute(query)
        return SampleReturn(uuid=ret_uuid,**sample.dict())


@router.get('/samples')
async def get_samples() -> List[SampleReturn]:
    query = samples.select()
    ret = await db.fetch_all(query)
    return [SampleReturn(**r) for r in ret]
