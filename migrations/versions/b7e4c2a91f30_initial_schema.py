"""initial schema

Revision ID: b7e4c2a91f30
Revises:
Create Date: 2026-01-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7e4c2a91f30'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'submissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('kind', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('locale', sa.String(length=8), nullable=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('company', sa.String(length=200), nullable=True),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('phone', sa.String(length=64), nullable=True),
        sa.Column('country', sa.String(length=120), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('consent', sa.Boolean(), nullable=False),
        sa.Column('enquiry_type', sa.String(length=64), nullable=True),
        sa.Column('product', sa.String(length=64), nullable=True),
        sa.Column('quantity', sa.String(length=120), nullable=True),
        sa.Column('consultation', sa.Boolean(), nullable=True),
        sa.Column('product_lines', sa.String(length=300), nullable=True),
        sa.Column('volume', sa.String(length=120), nullable=True),
        sa.Column('frequency', sa.String(length=64), nullable=True),
        sa.Column('target_market', sa.String(length=200), nullable=True),
        sa.Column('ip', sa.String(length=64), nullable=True),
        sa.Column('user_agent', sa.String(length=400), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('submissions', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_submissions_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_submissions_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_submissions_kind'), ['kind'], unique=False)

    op.create_table(
        'analytics_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('type', sa.String(length=48), nullable=False),
        sa.Column('path', sa.String(length=500), nullable=True),
        sa.Column('referrer', sa.String(length=500), nullable=True),
        sa.Column('locale', sa.String(length=8), nullable=True),
        sa.Column('session_id', sa.String(length=64), nullable=True),
        sa.Column('meta', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('analytics_events', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_analytics_events_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_analytics_events_session_id'), ['session_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_analytics_events_type'), ['type'], unique=False)


def downgrade():
    with op.batch_alter_table('analytics_events', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_analytics_events_type'))
        batch_op.drop_index(batch_op.f('ix_analytics_events_session_id'))
        batch_op.drop_index(batch_op.f('ix_analytics_events_created_at'))
    op.drop_table('analytics_events')

    with op.batch_alter_table('submissions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_submissions_kind'))
        batch_op.drop_index(batch_op.f('ix_submissions_email'))
        batch_op.drop_index(batch_op.f('ix_submissions_created_at'))
    op.drop_table('submissions')
