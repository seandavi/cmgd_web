#!/usr/bin/env python3
import uuid
from fastapi import APIRouter, File, UploadFile
from typing import List
from pydantic import BaseModel, Field

from ..models.samples import *
from .metadata_tsv_files import MetadataTSVFile

router = APIRouter()


def init_app(app):
    app.include_router(router, prefix='/samples')



@router.get('/samples')
def get_samples():
    sel = samples.select()
    return str(sel)


@router.post("/metadata_csv")
async def create_metadata_from_csv(files: List[UploadFile] = File(...)):
    x = []
    for f in files:
        x.append(MetadataTSVFile(f.file).samples)
    #return {"filenames": [file.filename for file in files]}
    print(x)
    return {'files': [y.to_dict('records') for y in x]}
