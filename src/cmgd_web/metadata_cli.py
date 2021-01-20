import uuid
from typing import List

import pandas as pd
import click
import orjson

BASE_UUID=uuid.UUID('00000000000000000000000000000000')


@click.group()
def group():
    pass

def uuid_from_srrs(srrs: List) -> uuid:
    res = uuid.uuid5(BASE_UUID,' '.join(sorted(srrs)))
    return str(res)


def uuid_from_metadata(fname):
    res = pd.read_csv(fname,sep="\t")
    res['uuid'] = res.apply(lambda row: uuid_from_srrs(row.NCBI_accession.split(';')),axis=1)
    return(res)

@group.command()
@click.argument('study_name')
@click.argument('fname')
def add_uuid_column(fname,study_name):
    try:
        res = uuid_from_metadata(fname)
        res['study_name']=study_name
        print(res.to_json(orient='records', lines=True))
    except:
        pass

if __name__ == '__main__':
    group()
