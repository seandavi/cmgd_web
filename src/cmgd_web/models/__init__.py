import sqlalchemy
import databases
import json

from .. import config

# db = Gino(
#     dsn=config.DB_DSN,
#     pool_min_size=config.DB_POOL_MIN_SIZE,
#     pool_max_size=config.DB_POOL_MAX_SIZE,
#     echo=config.DB_ECHO,
#     ssl=config.DB_SSL,
#     use_connection_for_request=config.DB_USE_CONNECTION_FOR_REQUEST,
#     retry_limit=config.DB_RETRY_LIMIT,
#     retry_interval=config.DB_RETRY_INTERVAL,
# )

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
