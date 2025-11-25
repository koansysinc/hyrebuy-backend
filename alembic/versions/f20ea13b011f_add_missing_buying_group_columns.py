"""add_missing_buying_group_columns

Revision ID: f20ea13b011f
Revises: fe00afe28a95
Create Date: 2025-11-25 08:04:21.704140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f20ea13b011f'
down_revision = 'fe00afe28a95'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add only the missing columns to buying_groups table
    op.add_column('buying_groups', sa.Column('target_configuration', sa.String(length=50), nullable=True))
    op.add_column('buying_groups', sa.Column('committed_member_count', sa.String(), server_default='0', nullable=False))
    op.add_column('buying_groups', sa.Column('selected_builder_id', sa.UUID(), nullable=True))
    op.add_column('buying_groups', sa.Column('final_discount_percent', sa.String(), nullable=True))
    op.add_column('buying_groups', sa.Column('final_price_per_unit', sa.BigInteger(), nullable=True))
    op.add_column('buying_groups', sa.Column('deal_closed_date', sa.Date(), nullable=True))
    op.add_column('buying_groups', sa.Column('public_landing_page_url', sa.String(), nullable=True))
    op.add_column('buying_groups', sa.Column('is_discoverable', sa.String(), server_default='1', nullable=False))

    # Add indexes
    op.create_index('idx_groups_admin', 'buying_groups', ['admin_id'], unique=False)
    op.create_index('idx_groups_status', 'buying_groups', ['status'], unique=False)

    # Add foreign key
    op.create_foreign_key('fk_buying_groups_builder', 'buying_groups', 'builders', ['selected_builder_id'], ['id'])


def downgrade() -> None:
    # Remove foreign key
    op.drop_constraint('fk_buying_groups_builder', 'buying_groups', type_='foreignkey')

    # Remove indexes
    op.drop_index('idx_groups_status', table_name='buying_groups')
    op.drop_index('idx_groups_admin', table_name='buying_groups')

    # Remove columns
    op.drop_column('buying_groups', 'is_discoverable')
    op.drop_column('buying_groups', 'public_landing_page_url')
    op.drop_column('buying_groups', 'deal_closed_date')
    op.drop_column('buying_groups', 'final_price_per_unit')
    op.drop_column('buying_groups', 'final_discount_percent')
    op.drop_column('buying_groups', 'selected_builder_id')
    op.drop_column('buying_groups', 'committed_member_count')
    op.drop_column('buying_groups', 'target_configuration')
