"""add storage

Revision ID: a1b39c75c083
Revises: ed23228a385c
Create Date: 2020-09-20 06:31:48.119042

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1b39c75c083'
down_revision = 'ed23228a385c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('storage_events',
    sa.Column('event_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('kind', sa.String(), nullable=True),
    sa.Column('id', sa.String(), nullable=True),
    sa.Column('self_link', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True, comment='file basename'),
    sa.Column('bucket', sa.String(), nullable=True, comment='simple bucket name'),
    sa.Column('generation', sa.BigInteger(), nullable=True),
    sa.Column('metageneration', sa.Integer(), nullable=True),
    sa.Column('content_type', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('size', sa.BigInteger(), nullable=True),
    sa.Column('md5_hash', sa.String(), nullable=True),
    sa.Column('media_link', sa.String(), nullable=True),
    sa.Column('content_language', sa.String(), nullable=True),
    sa.Column('crc32c', sa.String(), nullable=True),
    sa.Column('etag', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('event_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('storage_events')
    # ### end Alembic commands ###