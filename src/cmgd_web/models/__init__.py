import sqlalchemy
import databases
import json

from .. import config

db = databases.Database(config.DB_DSN)

def json_loads(v):
    return json.loads(v)


def serialize_unknown_types(v):
    return str(v)


def json_dumps(v, *, default=serialize_unknown_types):
    return json.dumps(v, default=default)

# HACCCCCKKKKYYYY
db._backend._dialect._jsonb_serializer = json_dumps
db._backend._dialect._jsonb_deserializer = json_loads

metadata = sqlalchemy.MetaData()
