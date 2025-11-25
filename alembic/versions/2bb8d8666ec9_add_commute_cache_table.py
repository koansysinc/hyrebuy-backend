"""add_commute_cache_table

Revision ID: 2bb8d8666ec9
Revises: 001
Create Date: 2025-11-25 07:30:26.304017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bb8d8666ec9'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'commute_cache',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('origin_lat', sa.Float(), nullable=False),
        sa.Column('origin_lng', sa.Float(), nullable=False),
        sa.Column('dest_lat', sa.Float(), nullable=False),
        sa.Column('dest_lng', sa.Float(), nullable=False),
        sa.Column('travel_mode', sa.String(length=20), nullable=False, server_default='driving'),
        sa.Column('distance_meters', sa.Integer(), nullable=False),
        sa.Column('distance_text', sa.String(length=50), nullable=False),
        sa.Column('duration_seconds', sa.Integer(), nullable=False),
        sa.Column('duration_text', sa.String(length=50), nullable=False),
        sa.Column('duration_in_traffic_seconds', sa.Integer(), nullable=True),
        sa.Column('duration_in_traffic_text', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index for fast lookups
    op.create_index(
        'idx_commute_lookup',
        'commute_cache',
        ['origin_lat', 'origin_lng', 'dest_lat', 'dest_lng', 'travel_mode']
    )


def downgrade() -> None:
    op.drop_index('idx_commute_lookup', table_name='commute_cache')
    op.drop_table('commute_cache')
