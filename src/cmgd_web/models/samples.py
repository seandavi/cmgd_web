import sqlalchemy as sa
import uuid


from . import metadata
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def init_app():
    pass

samples_to_studies = sa.Table(
    "samples_to_studies",
    metadata,
    sa.Column('sample_uuid',UUID, sa.ForeignKey("samples.uuid")),
    sa.Column('study_uuid',UUID, sa.ForeignKey("studies.uuid")),
    sa.UniqueConstraint('sample_uuid', 'study_uuid')
)

studies = sa.Table(
    'studies',
    metadata,
    sa.Column('uuid', UUID, primary_key = True,
                     server_default = sa.text('uuid_generate_v4()')),
    sa.Column('name',sa.String(), unique = True),
    sa.Column('pubmed',sa.Integer)
)


samples_to_sra_runs = sa.Table(
    "samples_to_sra_runs",
    metadata,
    sa.Column("uuid", UUID, primary_key=True,
              server_default=text("uuid_generate_v4()")),
    sa.Column('sample_uuid',UUID, sa.ForeignKey("samples.uuid"),
              index=True),
    sa.Column('sra_run_uuid',UUID, sa.ForeignKey("sra_runs.uuid"),
              index=True),
    sa.UniqueConstraint('sample_uuid','sra_run_uuid')
)


samples_to_variables = sa.Table(
    "samples_to_variables",
    metadata,
    sa.Column('sample_uuid',UUID, sa.ForeignKey("samples.uuid"),
              index=True),
    sa.Column('variable_uuid',UUID, sa.ForeignKey("variables.uuid"),
              index=True),
    sa.UniqueConstraint('sample_uuid', 'variable_uuid')
)

samples = sa.Table(
    'samples',
    metadata,
    sa.Column('uuid',UUID, primary_key = True,
                     server_default = sa.text('uuid_generate_v4()')),
    sa.Column('name',sa.String(), unique = True),
    sa.Column('hash',sa.String(), unique=True, index=True,
                     comment = 'hash of sample identifiers')
)



sra_runs = sa.Table(
    'sra_runs',
    metadata,
    sa.Column('uuid',UUID, primary_key = True,
                     server_default = sa.text('uuid_generate_v4()')),
    sa.Column('accession', sa.String(), unique = True)
)

variables = sa.Table(
    'variables',
    metadata,
    sa.Column('uuid',UUID, primary_key = True,
                     server_default = sa.text('uuid_generate_v4()')),
    sa.Column('variable',sa.String(), index = True),
    sa.Column('value',sa.String(), index=True),
    sa.Column('var_type',sa.String, index = True)
    )
