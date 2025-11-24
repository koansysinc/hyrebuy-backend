"""
Script to create initial database migration
Run this to generate the migration file from models
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This would normally be: alembic revision --autogenerate -m "Initial schema"
# For now, we'll create the migration manually

print("To create migration, run:")
print("cd /home/koans/projects/hyrebuy/hyrebuy-backend")
print("alembic revision --autogenerate -m 'Initial schema with all Phase 1 tables'")
print("")
print("To apply migration, run:")
print("alembic upgrade head")
