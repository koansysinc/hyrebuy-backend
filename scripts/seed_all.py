"""
Master seed script - runs all seed scripts in correct order
Day 6: Database Seeding

1. GCC Companies (P1-F08)
2. Builders
3. Properties (P1-F04)
"""

import asyncio
import sys

# Import seed functions
from seed_gcc_companies import seed_gcc_companies
from seed_builders import seed_builders
from seed_properties import seed_properties


async def seed_all():
    """Run all seed scripts in order"""
    print("\n" + "=" * 70)
    print("HYREBUY DATABASE SEEDING - DAY 6")
    print("=" * 70)
    print("\nThis will seed:")
    print("  - 10 GCC Companies (P1-F08)")
    print("  - 10 Builders")
    print("  - 13 Properties (P1-F04)")
    print("\n" + "=" * 70)

    try:
        # Step 1: Seed GCC Companies
        print("\n[Step 1/3] Seeding GCC Companies...")
        await seed_gcc_companies()

        # Step 2: Seed Builders
        print("\n[Step 2/3] Seeding Builders...")
        await seed_builders()

        # Step 3: Seed Properties
        print("\n[Step 3/3] Seeding Properties...")
        await seed_properties()

        print("\n" + "=" * 70)
        print("✅ ALL SEED SCRIPTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nDatabase seeded with:")
        print("  ✅ 10 GCC Companies")
        print("  ✅ 10 Builders")
        print("  ✅ 13 Properties")
        print("\nReady for Week 2 development!")
        print("=" * 70 + "\n")

    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ SEED FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        print("\nPlease check:")
        print("  - Database is running")
        print("  - Migrations are applied (alembic upgrade head)")
        print("  - Connection string in .env is correct")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(seed_all())
