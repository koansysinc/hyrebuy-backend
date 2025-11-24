"""
Seed builders/developers in Hyderabad
Related to P1-F04: Property Database Seeding

Major real estate builders in Hyderabad
Data includes: name, description, rating, on-time delivery %, group buying support
"""

import sys
import os
import asyncio
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.models.builder import Builder


# Builders data - major real estate developers in Hyderabad
BUILDERS = [
    {
        "name": "Aparna Constructions",
        "description": "Leading real estate developer in Hyderabad with 30+ years of experience",
        "rating": "4.5",
        "total_projects": "85",
        "on_time_delivery_percentage": "92.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "5",
        "website": "https://www.aparnaconstructions.com",
        "contact_phone": "+91-40-44556677",
        "contact_email": "info@aparnaconstructions.com"
    },
    {
        "name": "My Home Group",
        "description": "Premium residential and commercial projects across Hyderabad",
        "rating": "4.6",
        "total_projects": "120",
        "on_time_delivery_percentage": "95.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "8",
        "website": "https://www.myhomegroup.in",
        "contact_phone": "+91-40-44332211",
        "contact_email": "sales@myhomegroup.in"
    },
    {
        "name": "Aliens Group",
        "description": "Innovative townships and gated communities in Hyderabad",
        "rating": "4.3",
        "total_projects": "45",
        "on_time_delivery_percentage": "88.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "10",
        "website": "https://www.aliensgroup.in",
        "contact_phone": "+91-40-44778899",
        "contact_email": "info@aliensgroup.in"
    },
    {
        "name": "Ramky Estates",
        "description": "Affordable and luxury housing across Hyderabad",
        "rating": "4.2",
        "total_projects": "95",
        "on_time_delivery_percentage": "85.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "6",
        "website": "https://www.ramkyestates.com",
        "contact_phone": "+91-40-44112233",
        "contact_email": "sales@ramkyestates.com"
    },
    {
        "name": "Prestige Group",
        "description": "Premium residential and commercial real estate developer",
        "rating": "4.7",
        "total_projects": "200",
        "on_time_delivery_percentage": "96.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "12",
        "website": "https://www.prestigeconstructions.com",
        "contact_phone": "+91-80-25591080",
        "contact_email": "info@prestigeconstructions.com"
    },
    {
        "name": "Kolte-Patil Developers",
        "description": "Trusted name in residential and commercial developments",
        "rating": "4.4",
        "total_projects": "75",
        "on_time_delivery_percentage": "90.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "7",
        "website": "https://www.koltepatil.com",
        "contact_phone": "+91-20-66226500",
        "contact_email": "customercare@koltepatil.com"
    },
    {
        "name": "Hallmark Builders",
        "description": "Quality homes with modern amenities in prime locations",
        "rating": "4.1",
        "total_projects": "38",
        "on_time_delivery_percentage": "83.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "5",
        "website": "https://www.hallmarkbuilders.in",
        "contact_phone": "+91-40-44998877",
        "contact_email": "info@hallmarkbuilders.in"
    },
    {
        "name": "Incor Group",
        "description": "Luxury residential projects with world-class amenities",
        "rating": "4.5",
        "total_projects": "42",
        "on_time_delivery_percentage": "91.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "10",
        "website": "https://www.incorgroup.com",
        "contact_phone": "+91-40-44556688",
        "contact_email": "sales@incorgroup.com"
    },
    {
        "name": "Vasavi Group",
        "description": "Trusted builder with focus on customer satisfaction",
        "rating": "4.3",
        "total_projects": "68",
        "on_time_delivery_percentage": "87.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "6",
        "website": "https://www.vasavigroup.com",
        "contact_phone": "+91-40-44223344",
        "contact_email": "info@vasavigroup.com"
    },
    {
        "name": "Lansum Properties",
        "description": "Premium gated communities with integrated amenities",
        "rating": "4.2",
        "total_projects": "28",
        "on_time_delivery_percentage": "86.0",
        "accepts_group_buying": "true",
        "minimum_group_size": "8",
        "website": "https://www.lansumproperties.com",
        "contact_phone": "+91-40-44667788",
        "contact_email": "sales@lansumproperties.com"
    }
]


async def seed_builders():
    """Seed builders into the database"""
    async with async_session_maker() as session:
        try:
            print("🏗️  Seeding builders...")

            for builder_data in BUILDERS:
                builder = Builder(
                    id=uuid.uuid4(),
                    name=builder_data["name"],
                    description=builder_data["description"],
                    rating=builder_data["rating"],
                    total_projects=builder_data["total_projects"],
                    on_time_delivery_percentage=builder_data["on_time_delivery_percentage"],
                    accepts_group_buying=builder_data["accepts_group_buying"],
                    minimum_group_size=builder_data["minimum_group_size"],
                    website=builder_data.get("website"),
                    contact_phone=builder_data.get("contact_phone"),
                    contact_email=builder_data.get("contact_email")
                )

                session.add(builder)
                print(f"  ✅ Added: {builder_data['name']} (Rating: {builder_data['rating']})")

            await session.commit()
            print(f"\n✅ Successfully seeded {len(BUILDERS)} builders!")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding builders: {e}")
            raise


if __name__ == "__main__":
    print("=" * 60)
    print("Builders Seed Script")
    print("=" * 60)
    asyncio.run(seed_builders())
