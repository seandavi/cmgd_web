"""base models

Revision ID: ed23228a385c
Revises: 
Create Date: 2020-09-16 22:11:18.843439

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ed23228a385c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('create extension "uuid-ossp"')
    op.create_table('nextflow_events',
    sa.Column('event_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('run_name', sa.String(), nullable=True),
    sa.Column('run_id', postgresql.UUID(), nullable=True),
    sa.Column('utc_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('event', sa.String(), nullable=True),
    sa.Column('trace', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('nickname', sa.Unicode(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('nextflow_events')
    # ### end Alembic commands ###
