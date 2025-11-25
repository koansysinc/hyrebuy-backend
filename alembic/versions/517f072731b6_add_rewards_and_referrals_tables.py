"""add_rewards_and_referrals_tables

Revision ID: 517f072731b6
Revises: ca6fac2a6459
Create Date: 2025-11-25 08:55:19.660588

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '517f072731b6'
down_revision = 'ca6fac2a6459'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create referrals table
    op.create_table('referrals',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('referrer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('referred_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('referral_code', sa.String(length=20), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=20), server_default='pending', nullable=False),
        sa.Column('conversion_type', sa.String(length=50), nullable=True),
        sa.Column('points_awarded', sa.Integer(), server_default='0', nullable=False),
        sa.Column('points_awarded_to_referrer', sa.Integer(), server_default='0', nullable=False),
        sa.Column('points_awarded_to_referred', sa.Integer(), server_default='0', nullable=False),
        sa.Column('referred_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('converted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['referrer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['referred_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_referrals_referrer', 'referrals', ['referrer_id'], unique=False)
    op.create_index('idx_referrals_referred', 'referrals', ['referred_id'], unique=False)
    op.create_index('idx_referrals_code', 'referrals', ['referral_code'], unique=False)
    op.create_index('idx_referrals_status', 'referrals', ['status'], unique=False)

    # Create reward_transactions table
    op.create_table('reward_transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action_type', sa.String(length=50), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('related_referral_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('related_group_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('related_property_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('balance_after', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['related_referral_id'], ['referrals.id'], ),
        sa.ForeignKeyConstraint(['related_group_id'], ['buying_groups.id'], ),
        sa.ForeignKeyConstraint(['related_property_id'], ['properties.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_reward_txn_user', 'reward_transactions', ['user_id'], unique=False)
    op.create_index('idx_reward_txn_action', 'reward_transactions', ['action_type'], unique=False)
    op.create_index('idx_reward_txn_created', 'reward_transactions', ['created_at'], unique=False)

    # Create user_reward_levels table
    op.create_table('user_reward_levels',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('current_level', sa.String(length=20), server_default='bronze', nullable=False),
        sa.Column('current_points', sa.Integer(), server_default='0', nullable=False),
        sa.Column('lifetime_points', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_referrals', sa.Integer(), server_default='0', nullable=False),
        sa.Column('successful_referrals', sa.Integer(), server_default='0', nullable=False),
        sa.Column('groups_created', sa.Integer(), server_default='0', nullable=False),
        sa.Column('groups_joined', sa.Integer(), server_default='0', nullable=False),
        sa.Column('properties_viewed', sa.Integer(), server_default='0', nullable=False),
        sa.Column('properties_saved', sa.Integer(), server_default='0', nullable=False),
        sa.Column('leaderboard_rank', sa.Integer(), nullable=True),
        sa.Column('level_achieved_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_user_reward_user', 'user_reward_levels', ['user_id'], unique=False)
    op.create_index('idx_user_reward_level', 'user_reward_levels', ['current_level'], unique=False)
    op.create_index('idx_user_reward_points', 'user_reward_levels', ['current_points'], unique=False)
    op.create_index('idx_user_reward_rank', 'user_reward_levels', ['leaderboard_rank'], unique=False)


def downgrade() -> None:
    # Drop user_reward_levels table
    op.drop_index('idx_user_reward_rank', table_name='user_reward_levels')
    op.drop_index('idx_user_reward_points', table_name='user_reward_levels')
    op.drop_index('idx_user_reward_level', table_name='user_reward_levels')
    op.drop_index('idx_user_reward_user', table_name='user_reward_levels')
    op.drop_table('user_reward_levels')

    # Drop reward_transactions table
    op.drop_index('idx_reward_txn_created', table_name='reward_transactions')
    op.drop_index('idx_reward_txn_action', table_name='reward_transactions')
    op.drop_index('idx_reward_txn_user', table_name='reward_transactions')
    op.drop_table('reward_transactions')

    # Drop referrals table
    op.drop_index('idx_referrals_status', table_name='referrals')
    op.drop_index('idx_referrals_code', table_name='referrals')
    op.drop_index('idx_referrals_referred', table_name='referrals')
    op.drop_index('idx_referrals_referrer', table_name='referrals')
    op.drop_table('referrals')
