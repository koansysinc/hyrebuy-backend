"""add_group_buying_tables

Revision ID: fe00afe28a95
Revises: 2bb8d8666ec9
Create Date: 2025-11-25 07:46:30.937343

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fe00afe28a95'
down_revision = '2bb8d8666ec9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create buying_groups table
    op.create_table(
        'buying_groups',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('admin_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('target_location', sa.String(length=100), nullable=False),
        sa.Column('target_configuration', sa.String(length=50), nullable=True),
        sa.Column('budget_min', sa.BigInteger(), nullable=True),
        sa.Column('budget_max', sa.BigInteger(), nullable=False),
        sa.Column('preferred_builders', postgresql.ARRAY(sa.UUID()), nullable=True),
        sa.Column('minimum_members', sa.String(), nullable=True, server_default='5'),
        sa.Column('maximum_members', sa.String(), nullable=True, server_default='20'),
        sa.Column('close_by_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True, server_default='forming'),
        sa.Column('current_member_count', sa.String(), nullable=True, server_default='1'),
        sa.Column('committed_member_count', sa.String(), nullable=True, server_default='0'),
        sa.Column('expected_discount_percent', sa.String(), nullable=True),
        sa.Column('current_discount_tier', sa.String(length=20), nullable=True),
        sa.Column('selected_builder_id', sa.UUID(), nullable=True),
        sa.Column('final_discount_percent', sa.String(), nullable=True),
        sa.Column('final_price_per_unit', sa.BigInteger(), nullable=True),
        sa.Column('deal_closed_date', sa.Date(), nullable=True),
        sa.Column('invite_code', sa.String(length=20), nullable=False),
        sa.Column('public_landing_page_url', sa.String(), nullable=True),
        sa.Column('is_discoverable', sa.String(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['admin_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['selected_builder_id'], ['builders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_groups_admin', 'buying_groups', ['admin_id'])
    op.create_index('idx_groups_location', 'buying_groups', ['target_location'])
    op.create_index('idx_groups_status', 'buying_groups', ['status'])
    op.create_index(op.f('ix_buying_groups_invite_code'), 'buying_groups', ['invite_code'], unique=True)

    # Create group_members table
    op.create_table(
        'group_members',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('group_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True, server_default='invited'),
        sa.Column('commitment_level', sa.String(), nullable=True, server_default='0'),
        sa.Column('invited_by', sa.UUID(), nullable=True),
        sa.Column('invited_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('committed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deposit_paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deposit_amount', sa.String(), nullable=True),
        sa.Column('selected_property_id', sa.UUID(), nullable=True),
        sa.Column('last_active_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('engagement_score', sa.String(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['buying_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['invited_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['selected_property_id'], ['properties.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_members_group', 'group_members', ['group_id'])
    op.create_index('idx_members_status', 'group_members', ['group_id', 'status'])
    op.create_index('idx_members_unique', 'group_members', ['group_id', 'user_id'], unique=True)
    op.create_index('idx_members_user', 'group_members', ['user_id'])

    # Create group_invites table
    op.create_table(
        'group_invites',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('group_id', sa.UUID(), nullable=False),
        sa.Column('inviter_id', sa.UUID(), nullable=False),
        sa.Column('invitee_id', sa.UUID(), nullable=True),
        sa.Column('invite_code', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='pending'),
        sa.Column('sharing_method', sa.String(length=20), nullable=True),
        sa.Column('accepted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('declined_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['buying_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['invitee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['inviter_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_invites_code', 'group_invites', ['invite_code'])
    op.create_index('idx_invites_group', 'group_invites', ['group_id'])
    op.create_index('idx_invites_inviter', 'group_invites', ['inviter_id'])
    op.create_index('idx_invites_status', 'group_invites', ['status'])
    op.create_index(op.f('ix_group_invites_invite_code'), 'group_invites', ['invite_code'], unique=True)

    # Create group_messages table
    op.create_table(
        'group_messages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('group_id', sa.UUID(), nullable=False),
        sa.Column('sender_id', sa.UUID(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(length=20), nullable=True, server_default='text'),
        sa.Column('is_pinned', sa.String(), nullable=True, server_default='false'),
        sa.Column('is_deleted', sa.String(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['buying_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_created', 'group_messages', ['group_id', 'created_at'])
    op.create_index('idx_messages_group', 'group_messages', ['group_id'])
    op.create_index('idx_messages_sender', 'group_messages', ['sender_id'])


def downgrade() -> None:
    # Drop tables in reverse order (child tables first)
    op.drop_index('idx_messages_sender', table_name='group_messages')
    op.drop_index('idx_messages_group', table_name='group_messages')
    op.drop_index('idx_messages_created', table_name='group_messages')
    op.drop_table('group_messages')

    op.drop_index(op.f('ix_group_invites_invite_code'), table_name='group_invites')
    op.drop_index('idx_invites_status', table_name='group_invites')
    op.drop_index('idx_invites_inviter', table_name='group_invites')
    op.drop_index('idx_invites_group', table_name='group_invites')
    op.drop_index('idx_invites_code', table_name='group_invites')
    op.drop_table('group_invites')

    op.drop_index('idx_members_user', table_name='group_members')
    op.drop_index('idx_members_unique', table_name='group_members')
    op.drop_index('idx_members_status', table_name='group_members')
    op.drop_index('idx_members_group', table_name='group_members')
    op.drop_table('group_members')

    op.drop_index(op.f('ix_buying_groups_invite_code'), table_name='buying_groups')
    op.drop_index('idx_groups_status', table_name='buying_groups')
    op.drop_index('idx_groups_location', table_name='buying_groups')
    op.drop_index('idx_groups_admin', table_name='buying_groups')
    op.drop_table('buying_groups')
