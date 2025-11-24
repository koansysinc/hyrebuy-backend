"""Initial schema with all Phase 1 tables

Revision ID: 001
Revises:
Create Date: 2025-11-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_group_admin', sa.String(length=10), server_default='false', nullable=True),
        sa.Column('total_rewards_earned', sa.String(), server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create gcc_companies table
    op.create_table(
        'gcc_companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('short_name', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('office_address', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=False),
        sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=False),
        sa.Column('employee_count', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_gcc_companies_location', 'gcc_companies', ['location'])
    op.create_index('ix_gcc_companies_name', 'gcc_companies', ['name'], unique=True)

    # Create builders table
    op.create_table(
        'builders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('rating', sa.String(), server_default='0.0', nullable=True),
        sa.Column('total_projects', sa.String(), server_default='0', nullable=True),
        sa.Column('on_time_delivery_percentage', sa.String(), server_default='0.0', nullable=True),
        sa.Column('accepts_group_buying', sa.String(length=10), server_default='false', nullable=True),
        sa.Column('minimum_group_size', sa.String(), server_default='5', nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('contact_phone', sa.String(length=20), nullable=True),
        sa.Column('contact_email', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_builders_name', 'builders', ['name'], unique=True)
    op.create_index('ix_builders_accepts_group', 'builders', ['accepts_group_buying'])

    # Create properties table
    op.create_table(
        'properties',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('builder_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=False),
        sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=False),
        sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=False),
        sa.Column('configuration', sa.String(length=50), nullable=False),
        sa.Column('carpet_area', sa.String(), nullable=False),
        sa.Column('price', sa.BigInteger(), nullable=False),
        sa.Column('price_per_sqft', sa.String(), nullable=True),
        sa.Column('smart_score', sa.Numeric(precision=5, scale=2), server_default='0.0', nullable=True),
        sa.Column('location_score', sa.Numeric(precision=5, scale=2), server_default='0.0', nullable=True),
        sa.Column('builder_score', sa.Numeric(precision=5, scale=2), server_default='0.0', nullable=True),
        sa.Column('price_score', sa.Numeric(precision=5, scale=2), server_default='0.0', nullable=True),
        sa.Column('commute_score', sa.Numeric(precision=5, scale=2), server_default='0.0', nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('amenities', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('images', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('supports_group_buying', sa.String(length=10), server_default='false', nullable=True),
        sa.Column('group_discount_percentage', sa.String(), nullable=True),
        sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['builder_id'], ['builders.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_properties_location', 'properties', ['location'])
    op.create_index('ix_properties_price', 'properties', ['price'])
    op.create_index('idx_properties_location_price', 'properties', ['location', 'price'])
    op.create_index('idx_properties_search_vector', 'properties', ['search_vector'], postgresql_using='gin')
    op.create_index('idx_properties_smart_score', 'properties', ['smart_score'])

    # Create commute_scores table
    op.create_table(
        'commute_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('property_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('distance_km', sa.Numeric(precision=8, scale=2), nullable=False),
        sa.Column('duration_seconds', sa.String(), nullable=False),
        sa.Column('normal_minutes', sa.String(), nullable=False),
        sa.Column('peak_morning_minutes', sa.String(), nullable=False),
        sa.Column('peak_evening_minutes', sa.String(), nullable=False),
        sa.Column('current_minutes', sa.String(), nullable=False),
        sa.Column('traffic_level', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['gcc_companies.id']),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_commute_scores_property_company', 'commute_scores', ['property_id', 'company_id'], unique=True)

    # Create buying_groups table
    op.create_table(
        'buying_groups',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('admin_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('target_location', sa.String(length=100), nullable=False),
        sa.Column('budget_min', sa.BigInteger(), nullable=True),
        sa.Column('budget_max', sa.BigInteger(), nullable=False),
        sa.Column('preferred_builders', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('minimum_members', sa.String(), server_default='5', nullable=True),
        sa.Column('maximum_members', sa.String(), server_default='20', nullable=True),
        sa.Column('status', sa.String(length=50), server_default='forming', nullable=True),
        sa.Column('current_member_count', sa.String(), server_default='1', nullable=True),
        sa.Column('invite_code', sa.String(length=20), nullable=False),
        sa.Column('expected_discount_percent', sa.String(), nullable=True),
        sa.Column('current_discount_tier', sa.String(length=20), nullable=True),
        sa.Column('close_by_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['admin_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_buying_groups_status', 'buying_groups', ['status'])
    op.create_index('ix_buying_groups_invite_code', 'buying_groups', ['invite_code'], unique=True)
    op.create_index('idx_groups_location', 'buying_groups', ['target_location'])

    # Create group_members table
    op.create_table(
        'group_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=50), server_default='invited', nullable=True),
        sa.Column('commitment_level', sa.String(), server_default='0', nullable=True),
        sa.Column('invited_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('invited_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('committed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deposit_paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deposit_amount', sa.String(), nullable=True),
        sa.Column('selected_property_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('last_active_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('engagement_score', sa.String(), server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['buying_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['invited_by'], ['users.id']),
        sa.ForeignKeyConstraint(['selected_property_id'], ['properties.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_members_group', 'group_members', ['group_id'])
    op.create_index('idx_members_user', 'group_members', ['user_id'])
    op.create_index('idx_members_status', 'group_members', ['group_id', 'status'])
    op.create_index('idx_members_unique', 'group_members', ['group_id', 'user_id'], unique=True)

    # Create saved_properties table
    op.create_table(
        'saved_properties',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('property_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('saved_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_saved_user', 'saved_properties', ['user_id'])
    op.create_index('idx_saved_property', 'saved_properties', ['property_id'])
    op.create_index('idx_saved_unique', 'saved_properties', ['user_id', 'property_id'], unique=True)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('saved_properties')
    op.drop_table('group_members')
    op.drop_table('buying_groups')
    op.drop_table('commute_scores')
    op.drop_table('properties')
    op.drop_table('builders')
    op.drop_table('gcc_companies')
    op.drop_table('users')
