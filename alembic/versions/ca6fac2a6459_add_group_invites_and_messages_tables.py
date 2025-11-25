"""add_group_invites_and_messages_tables

Revision ID: ca6fac2a6459
Revises: f20ea13b011f
Create Date: 2025-11-25 08:15:49.233821

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ca6fac2a6459'
down_revision = 'f20ea13b011f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create group_invites table
    op.create_table('group_invites',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('inviter_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invitee_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('invite_code', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='pending', nullable=False),
        sa.Column('sharing_method', sa.String(length=20), nullable=True),
        sa.Column('whatsapp_link', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['buying_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['inviter_id'], ['users.id']),
        sa.ForeignKeyConstraint(['invitee_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_invites_code', 'group_invites', ['invite_code'], unique=True)
    op.create_index('idx_invites_group', 'group_invites', ['group_id'], unique=False)
    op.create_index('idx_invites_status', 'group_invites', ['status'], unique=False)

    # Create group_messages table
    op.create_table('group_messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sender_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(length=20), server_default='text', nullable=False),
        sa.Column('is_pinned', sa.String(length=10), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['buying_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_group', 'group_messages', ['group_id'], unique=False)
    op.create_index('idx_messages_created', 'group_messages', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop group_messages table
    op.drop_index('idx_messages_created', table_name='group_messages')
    op.drop_index('idx_messages_group', table_name='group_messages')
    op.drop_table('group_messages')

    # Drop group_invites table
    op.drop_index('idx_invites_status', table_name='group_invites')
    op.drop_index('idx_invites_group', table_name='group_invites')
    op.drop_index('idx_invites_code', table_name='group_invites')
    op.drop_table('group_invites')
