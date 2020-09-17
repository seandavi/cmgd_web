#!/usr/bin/env python3
from . import db
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import DateTime, text


class NextflowEvent(db.Model):
    __tablename__ = "nextflow_events"

    event_id = db.Column(UUID, primary_key=True,
                         server_default=text("uuid_generate_v4()"))
    run_name = db.Column(db.String())
    run_id = db.Column(UUID)
    utc_time = db.Column(db.DateTime(timezone=True))
    event = db.Column(db.String()) # TODO: split out to separate table (enum)
    trace = db.Column(JSONB)
    metadata = db.Column(JSONB)

