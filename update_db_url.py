#!/usr/bin/env python3
"""
Helper script to update DATABASE_URL in .env file
Usage: python update_db_url.py "your-vercel-connection-string"
"""

import sys
import os
from pathlib import Path

def convert_vercel_url_to_asyncpg(vercel_url: str) -> str:
    """
    Convert Vercel Postgres URL to AsyncPG format

    Input: postgresql://default:password@host:5432/verceldb
    Output: postgresql+asyncpg://default:password@host:5432/verceldb?ssl=require
    """
    # Remove any existing query parameters
    base_url = vercel_url.split('?')[0]

    # Replace postgresql:// with postgresql+asyncpg://
    if base_url.startswith('postgresql://'):
        asyncpg_url = base_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
    else:
        asyncpg_url = base_url

    # Add SSL requirement
    if '?' in asyncpg_url:
        asyncpg_url += '&ssl=require'
    else:
        asyncpg_url += '?ssl=require'

    return asyncpg_url


def update_env_file(new_database_url: str):
    """Update .env file with new DATABASE_URL"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print(f"❌ Error: .env file not found at {env_path}")
        print("Creating new .env file...")
        env_path.touch()

    # Read existing .env content
    with open(env_path, 'r') as f:
        lines = f.readlines()

    # Update or add DATABASE_URL
    updated = False
    new_lines = []

    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append(f'DATABASE_URL={new_database_url}\n')
            updated = True
            print(f"✅ Updated existing DATABASE_URL")
        else:
            new_lines.append(line)

    # If DATABASE_URL wasn't found, add it
    if not updated:
        new_lines.append(f'\nDATABase_URL={new_database_url}\n')
        print(f"✅ Added new DATABASE_URL")

    # Write back to .env
    with open(env_path, 'w') as f:
        f.writelines(new_lines)

    print(f"\n✅ .env file updated successfully!")
    print(f"Location: {env_path}")
    print(f"\nNew DATABASE_URL:")
    print(f"{new_database_url}")


def main():
    if len(sys.argv) < 2:
        print("❌ Error: No connection string provided")
        print("\nUsage:")
        print('  python update_db_url.py "postgresql://default:password@host:5432/verceldb"')
        print("\nOr with asyncpg format:")
        print('  python update_db_url.py "postgresql+asyncpg://default:password@host:5432/verceldb?ssl=require"')
        sys.exit(1)

    vercel_url = sys.argv[1]

    print("🔄 Converting Vercel URL to AsyncPG format...")
    print(f"\nInput URL: {vercel_url[:50]}...")

    # Convert to asyncpg format
    asyncpg_url = convert_vercel_url_to_asyncpg(vercel_url)

    print(f"\nConverted URL: {asyncpg_url[:50]}...")

    # Update .env file
    update_env_file(asyncpg_url)

    print("\n" + "="*70)
    print("Next Steps:")
    print("="*70)
    print("1. Test connection:")
    print("   python -c \"from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('DATABASE_URL'))\"")
    print("\n2. Run migrations:")
    print("   alembic upgrade head")
    print("\n3. Run seed scripts:")
    print("   python scripts/seed_all.py")
    print("\n4. Start backend:")
    print("   uvicorn app.main:app --reload")
    print("="*70)


if __name__ == '__main__':
    main()
