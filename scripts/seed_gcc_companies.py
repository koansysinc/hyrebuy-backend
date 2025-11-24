"""
Seed GCC companies in Hyderabad
P1-F08: GCC Company Seeding

Major tech companies with offices in Hyderabad
Data includes: name, location, office address, latitude, longitude
"""

import sys
import os
import asyncio
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.models.gcc_company import GCCCompany


# GCC Companies data - major tech companies in Hyderabad
GCC_COMPANIES = [
    {
        "name": "Amazon Development Centre",
        "short_name": "Amazon",
        "location": "Gachibowli",
        "office_address": "Survey No. 64, Nanakramguda Village, Serilingampally Mandal, Hyderabad, 500032",
        "latitude": "17.4408",
        "longitude": "78.3831",
        "employee_count": "15000"
    },
    {
        "name": "Google India",
        "short_name": "Google",
        "location": "Gachibowli",
        "office_address": "DivyaSree Omega, Kondapur, Hyderabad, 500084",
        "latitude": "17.4595",
        "longitude": "78.3675",
        "employee_count": "8000"
    },
    {
        "name": "Microsoft India Development Center",
        "short_name": "Microsoft",
        "location": "Gachibowli",
        "office_address": "Building 3, DLF Cyber City, Gachibowli, Hyderabad, 500032",
        "latitude": "17.4280",
        "longitude": "78.3479",
        "employee_count": "12000"
    },
    {
        "name": "Apple India",
        "short_name": "Apple",
        "location": "Hitech City",
        "office_address": "RMZ Futura, Hitech City, Hyderabad, 500081",
        "latitude": "17.4434",
        "longitude": "78.3772",
        "employee_count": "5000"
    },
    {
        "name": "Facebook India (Meta)",
        "short_name": "Meta",
        "location": "Gachibowli",
        "office_address": "Salarpuria Sattva Knowledge City, Raidurg, Hyderabad, 500081",
        "latitude": "17.4423",
        "longitude": "78.3700",
        "employee_count": "3000"
    },
    {
        "name": "Salesforce India",
        "short_name": "Salesforce",
        "location": "Gachibowli",
        "office_address": "Block 1, DivyaSree Omega, Kondapur, Hyderabad, 500084",
        "latitude": "17.4600",
        "longitude": "78.3680",
        "employee_count": "2500"
    },
    {
        "name": "Qualcomm India",
        "short_name": "Qualcomm",
        "location": "Hitech City",
        "office_address": "Survey No. 12, 13, 14, Hitech City, Madhapur, Hyderabad, 500081",
        "latitude": "17.4485",
        "longitude": "78.3908",
        "employee_count": "4000"
    },
    {
        "name": "Oracle India",
        "short_name": "Oracle",
        "location": "Gachibowli",
        "office_address": "Oracle Campus, Survey No. 7, Hitech City, Hyderabad, 500081",
        "latitude": "17.4365",
        "longitude": "78.3785",
        "employee_count": "6000"
    },
    {
        "name": "Deloitte India",
        "short_name": "Deloitte",
        "location": "Gachibowli",
        "office_address": "Raheja Mindspace, Hitech City, Madhapur, Hyderabad, 500081",
        "latitude": "17.4390",
        "longitude": "78.3870",
        "employee_count": "8000"
    },
    {
        "name": "Accenture India",
        "short_name": "Accenture",
        "location": "Gachibowli",
        "office_address": "DLF Cyber City, Gachibowli, Hyderabad, 500032",
        "latitude": "17.4267",
        "longitude": "78.3490",
        "employee_count": "10000"
    }
]


async def seed_gcc_companies():
    """Seed GCC companies into the database"""
    async with async_session_maker() as session:
        try:
            print("🏢 Seeding GCC companies...")

            for company_data in GCC_COMPANIES:
                company = GCCCompany(
                    id=uuid.uuid4(),
                    name=company_data["name"],
                    short_name=company_data["short_name"],
                    location=company_data["location"],
                    office_address=company_data["office_address"],
                    latitude=company_data["latitude"],
                    longitude=company_data["longitude"],
                    employee_count=company_data["employee_count"]
                )

                session.add(company)
                print(f"  ✅ Added: {company_data['name']} ({company_data['location']})")

            await session.commit()
            print(f"\n✅ Successfully seeded {len(GCC_COMPANIES)} GCC companies!")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding companies: {e}")
            raise


if __name__ == "__main__":
    print("=" * 60)
    print("GCC Companies Seed Script (P1-F08)")
    print("=" * 60)
    asyncio.run(seed_gcc_companies())
