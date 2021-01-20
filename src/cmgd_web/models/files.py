import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import DateTime, text
from sqlalchemy.ext.declarative import declarative_base

from . import metadata

Base = declarative_base()

class StorageEvent(Base):
    __tablename__ = "storage_events"

    event_id = sa.Column(UUID, primary_key=True,
                         server_default=text("uuid_generate_v4()"))
    kind = sa.Column(sa.String())
    id = sa.Column(sa.String())
    self_link = sa.Column(sa.String())
    name = sa.Column(sa.String(), comment="file basename")
    bucket = sa.Column(sa.String(), comment="simple bucket name")
    generation = sa.Column(sa.BigInteger())
    metageneration = sa.Column(sa.Integer())
    content_type = sa.Column(sa.String())
    created =  sa.Column(sa.DateTime(timezone=True))
    updated =  sa.Column(sa.DateTime(timezone=True))
    size = sa.Column(sa.BigInteger())
    md5_hash = sa.Column(sa.String())
    media_link = sa.Column(sa.String())
    content_language = sa.Column(sa.String())
    crc32c = sa.Column(sa.String())
    etag = sa.Column(sa.String())
    event_type = sa.Column(sa.String())
    event_time = sa.Column(sa.DateTime(timezone=True))
