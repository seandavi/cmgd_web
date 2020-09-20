from . import db
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import DateTime, text


class StorageEvent(db.Model):
    __tablename__ = "storage_events"

    event_id = db.Column(UUID, primary_key=True,
                         server_default=text("uuid_generate_v4()"))
    kind = db.Column(db.String())
    id = db.Column(db.String())
    self_link = db.Column(db.String())
    name = db.Column(db.String(), comment="file basename")
    bucket = db.Column(db.String(), comment="simple bucket name")
    generation = db.Column(db.BigInteger())
    metageneration = db.Column(db.Integer())
    content_type = db.Column(db.String())
    created =  db.Column(db.DateTime(timezone=True))
    updated =  db.Column(db.DateTime(timezone=True))
    size = db.Column(db.BigInteger())
    md5_hash = db.Column(db.String())
    media_link = db.Column(db.String())
    content_language = db.Column(db.String())
    crc32c = db.Column(db.String())
    etag = db.Column(db.String())
    event_type = db.Column(db.String())
    event_time = db.Column(db.DateTime(timezone=True))
