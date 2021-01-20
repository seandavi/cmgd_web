#!/usr/bin/env python3
from . import metadata
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import DateTime, text
from pydantic import BaseModel
import pydantic as pyd
import datetime
import typing

nextflow_event = sa.Table(
    "nextflow_events",
    metadata,
    sa.Column('event_id', UUID, primary_key=True,
              server_default = sa.text("uuid_generate_v4()")),
    sa.Column('run_name',sa.String()),
    sa.Column('run_id', UUID()),
    sa.Column("utc_time", sa.DateTime(timezone=True)),
    sa.Column("event", sa.String()),
    sa.Column("trace", JSONB()),
    sa.Column("metadata", JSONB())
)


nextflow_traces = sa.Table(
    "nextflow_traces",
    metadata,
    sa.Column("uuid", UUID, primary_key=True,
              server_default = sa.text("uuid_generate_v4()")),
    sa.Column("events_uuid", UUID(),
              sa.ForeignKey("nextflow_events.event_id"), index=True),
    sa.Column("env", sa.String()),
    sa.Column("rss", sa.Integer()),
    sa.Column("tag", sa.String()),
    sa.Column("cpus", sa.Float()),
    sa.Column("disk", sa.Float()),
    sa.Column("hash", sa.String()),
    sa.Column("name", sa.String()),
    sa.Column("queue", sa.String()),
    sa.Column("start", sa.DateTime(), index=True),
    sa.Column("rss", sa.Integer()),
    sa.Column("script", sa.String()),
    sa.Column("status", sa.String(), index=True),
    sa.Column("submit", sa.DateTime(), index=True),
    sa.Column("process", sa.String(), index=True),
    sa.Column("workdir", sa.String()),
    sa.Column("exit", sa.Integer(), index=True),
    sa.Column("attempt", sa.Integer()),
    sa.Column("scratch", sa.Integer()),
    sa.Column("container", sa.String(), index=True),
    sa.Column("native_id", sa.String()),
    sa.Column("scratch", sa.Integer()),
    sa.Column("task_id", sa.Integer(), index=True),
)

# high-level
#
#  pp

class NFTrace(BaseModel):
    env: str
    rss: int=None
    tag: str
    # pct_cpu (%cpu)
    cpus: float
    disk: float = None
    exit: int
    hash: str
    name: str
    queue: str
    start: datetime.datetime
    memory: int
    module: list=None
    script: str
    status: str
    submit: datetime.datetime
    attempt: int
    process: str
    scratch: int=None
    task_id: int
    workdir: str
    container: str=None
    native_id: str=None


workflow_process = sa.Table(
    "workflow_processes",
    metadata,
    sa.Column("uuid", UUID, primary_key=True,
              server_default = sa.text("uuid_generate_v4()")),
    sa.Column("workflows_uuid", UUID(),
              sa.ForeignKey("workflows.uuid"), index=True),
    sa.Column("hash",sa.String()),
    sa.Column("name",sa.String()),
    sa.Column("index",sa.Integer()),
    sa.Column("cached",sa.Integer()),
    sa.Column("failed",sa.Integer()),
    sa.Column("stored",sa.Integer()),
    sa.Column("aborted",sa.Integer()),
    sa.Column("errored",sa.Boolean()),
    sa.Column("ignored",sa.Integer()),
    sa.Column("pending",sa.Integer()),
    sa.Column("retries",sa.Integer()),
    sa.Column("running",sa.Integer()),
    sa.Column("loadCpus",sa.Integer()),
    sa.Column("peakCpus",sa.Integer()),
    sa.Column("submitted",sa.Integer()),
    sa.Column("succeeded",sa.Integer()),
    sa.Column("loadMemory",sa.Integer()),
    sa.Column("peakMemory",sa.Integer()),
    sa.Column("totalCount",sa.Integer()),
    sa.Column("taskName",sa.String()),
    sa.Column("terminated",sa.Boolean()),
    sa.Column("peakRunning",sa.Integer()),
    sa.Column("completedCount",sa.Integer()),
)

class WorkflowProcess(BaseModel):
    hash: str
    name: str
    index: int
    cached: int
    failed: int
    stored: int
    aborted: int
    errored: bool
    ignored: int
    pending: int
    retries: int
    running: int
    loadCpus: int
    peakCpus: int
    taskName: str
    submitted: int
    succeeded: int
    loadMemory: int
    peakMemory: int
    terminated: bool
    totalCount: int
    peakRunning: int
    completedCount: int


workflow_stats = sa.Table(
    "workflow_stats",
    metadata,
    # TODO: need foreign keys....
    sa.Column("loadCpus", sa.Integer()),
    sa.Column("peakCpus", sa.Integer()),
    sa.Column("cachedPct", sa.Float()),
    sa.Column("failedPnc", sa.Float()),
    sa.Column("processes", sa.Integer()), ## TODO: see list of processes
    sa.Column("ignoredPct", sa.Float()),
    sa.Column("loadMemory", sa.Integer()),
    sa.Column("peakMemory", sa.Integer()),
    sa.Column("succeedPct", sa.Float()),
    sa.Column("failedCout", sa.Integer()),
    sa.Column("peakRunning", sa.Integer()),
    sa.Column("abortedCount", sa.Integer()),
    sa.Column("ignoredCount", sa.Integer()),
    sa.Column("pendingCount", sa.Integer()),
    sa.Column("retriesCount", sa.Integer()),
    sa.Column("runningCount", sa.Integer()),
    sa.Column("loadMemoryFmt", sa.String()),
    sa.Column("peakMemoryFmt", sa.String()),
    sa.Column("CachedCountFmt", sa.String()),
    sa.Column("cachedDuration", sa.Integer()),
    sa.Column("computeTimeFmt", sa.String()),
    sa.Column("failedCountFmt", sa.String()),
    sa.Column("failedDuration", sa.Integer()),
    sa.Column("progressLength", sa.Integer()),
    sa.Column("submittedCount", sa.Integer()),
    sa.Column("succeededCount", sa.Integer()),
    sa.Column("changeTimestamp", sa.DateTime(timezone=True)),
    sa.Column("ignoredCountFmt", sa.String()),
    sa.Column("succeedCountFmt", sa.String()),
    sa.Column("succeedDuration", sa.Integer()),
    sa.Column("progressLength", sa.Integer()),
)

class NFMdWorkflowStats(BaseModel):
    loadCpus: int
    peakCpus: int
    cachedPct: float
    failedPct: float
    processes: typing.List[WorkflowProcess]
    ignoredPct: float
    loadMemory: int
    peakMemory: int
    succeedPct: float
    failedCount: int
    peakRunning: int
    abortedCount: int
    ignoredCount: int
    pendingCount: int
    retriesCount: int
    runningCount: int
    loadMemoryFmt: str
    peakMemoryFmt: str
    cachedCountFmt: str
    cachedDuration: int
    computeTimeFmt: str
    failedCountFmt: str
    failedDuration: int
    progressLength: int
    submittedCount: int
    succeededCount: int
    changeTimestamp: datetime.datetime
    ignoredCountFmt: str
    succeedCountFmt: str
    succeedDuration: int


workflows = sa.Table(
    "workflows",
    metadata,
    sa.Column("uuid", UUID(),primary_key=True,
              server_default = sa.text("uuid_generate_v4()")),
    sa.Column("commandLine", sa.String()),
    sa.Column("commitId", sa.String()),
    sa.Column("complete", JSONB()),
    sa.Column("configFiles", sa.ARRAY(sa.String)),
    sa.Column("container", sa.String()),
    sa.Column("containerEngine", sa.String())
)

class NFMdWorkflow(BaseModel):
    commandLine: str
    commitId: str=None
    complete: dict # time of completion
    configFiles: list=None
    container: str
    containerEngine: str
    duration: int
    errorMessage: str=None
    errorReport: str=None
    manifest: dict
    nextflow: dict
    success: bool
    userName: str=None
    workDir: str
    workflowStats: dict=None
    stats: NFMdWorkflowStats=None
    exitStatus: int=None
    homeDir: str
    launchDir: str
    profile: str=None
    projectDir: str
    projectName: str
    repository: str=None
    resume: bool
    revision: str=None
    runName: str
    scriptFile: str
    scriptName: str
    sessionId: pyd.UUID4
    start: dict # time of start

class NFMetadata(BaseModel):
    parameters: dict=None
    workflow: NFMdWorkflow=None

class NF(BaseModel):
    event: str
    event_id: pyd.UUID4=None
    run_name: str
    run_id: pyd.UUID4
    utc_time: datetime.datetime
    trace: NFTrace=None
    metadata: NFMetadata=None

# class NextflowEvent(db.Model):
#     __tablename__ = "nextflow_events"

#     event_id = db.Column(UUID, primary_key=True,
#                          server_default=text("uuid_generate_v4()"))
#     run_name = db.Column(db.String())
#     run_id = db.Column(UUID)
#     utc_time = db.Column(db.DateTime(timezone=True))
#     event = db.Column(db.String()) # TODO: split out to separate table (enum)
#     trace = db.Column(JSONB)
#     metadata = db.Column(JSONB)

# 'env',
# 'rss', 'tag', '%cpu', '%mem', 'cpus', 'disk', 'exit',
# 'hash', 'name', 'time', 'vmem', 'queue', 'rchar', 'start',
# 'syscr', 'syscw', 'wchar', 'memory', 'module', 'script',
# 'status', 'submit', 'attempt', 'process', 'scratch',
# 'task_id', 'workdir', 'complete', 'duration', 'inv_ctxt',
# 'peak_rss', 'realtime', 'vol_ctxt', 'container', 'native_id',
# 'peak_vmem', 'read_bytes', 'write_bytes', 'error_action'
